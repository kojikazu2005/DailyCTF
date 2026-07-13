
# Daily CTF Writeups

毎日1問、CTF の問題を解きながら学習を積み上げるリポジトリです。  
問題ファイルそのものは公開しませんが、  
**解法・コード・学び・試行錯誤**をまとめています。

---

##  目的
- 毎日違うジャンルの CTF を解いてスキルを広げる  
- 暗号・Web・Forensics・Pwn など幅広く挑戦  
- 学習ログを残し、成長を可視化する  
- ポートフォリオとして技術力を示す  

---

##  ディレクトリ構成


## Environment / Setup

### Docker-based Linux Environment
- Ubuntu 22.04
- pwndbg / gdb
- pwntools
- ROPgadget / one_gadget
- glibc / ELF toolchain

### Dockerコマンド
- コンテナ起動
docker start pwn-box

- コンテナに入る
docker exec -it pwn-box bash

- コンテナ停止・exit後
docker stop pwn-box

- コンテナ削除
docker rm pwn-box

- イメージ削除
docker rmi pwn-env

---

### Host (macOS)
- Apple Silicon
- VSCode
- Python 3.13.9
- Homebrew
