import server
import dis
import sys
print(dir(server))

#print(dis.dis(server))
"""
Disassembly of is_inside_the_typhoon_eye:
 19           0 LOAD_GLOBAL              0 (Path)
              2 LOAD_GLOBAL              1 (__file__)
              4 CALL_FUNCTION            1
              6 LOAD_METHOD              2 (resolve)
              8 CALL_METHOD              0
             10 LOAD_ATTR                3 (parent)
             12 LOAD_ATTR                4 (name)
             14 STORE_FAST               0 (current_place)

 20          16 LOAD_GLOBAL              5 (bytes)
             18 BUILD_LIST               0
             20 LOAD_CONST               1 ((101, 121, 101))
             22 LIST_EXTEND              1
             24 CALL_FUNCTION            1
             26 LOAD_METHOD              6 (decode)
             28 CALL_METHOD              0
             30 STORE_FAST               1 (required_place)

 21          32 LOAD_FAST                0 (current_place)
             34 LOAD_FAST                1 (required_place)
             36 COMPARE_OP               2 (==)
             38 RETURN_VALUE

Disassembly of main:
 36           0 LOAD_GLOBAL              0 (is_inside_the_typhoon_eye)
              2 CALL_FUNCTION            0
              4 POP_JUMP_IF_TRUE         9 (to 18)

 37           6 LOAD_GLOBAL              1 (print)
              8 LOAD_CONST               1 ('Hint: Move this file into the eye of the typhoon.')
             10 CALL_FUNCTION            1
             12 POP_TOP

 38          14 LOAD_CONST               0 (None)
             16 RETURN_VALUE

 40     >>   18 LOAD_GLOBAL              2 (input)
             20 LOAD_CONST               2 ('What was inside the eye? > ')
             22 CALL_FUNCTION            1
             24 STORE_FAST               0 (answer)

 42          26 LOAD_FAST                0 (answer)
             28 LOAD_GLOBAL              3 (reverse_the_wind)
             30 LOAD_GLOBAL              4 (EYE_DATA)
             32 CALL_FUNCTION            1
             34 COMPARE_OP               2 (==)
             36 POP_JUMP_IF_FALSE       25 (to 50)

 43          38 LOAD_GLOBAL              1 (print)
             40 LOAD_CONST               3 ('The typhoon is gone. Correct!')
             42 CALL_FUNCTION            1
             44 POP_TOP
             46 LOAD_CONST               0 (None)
             48 RETURN_VALUE

 45     >>   50 LOAD_GLOBAL              1 (print)
             52 LOAD_CONST               4 ('The wind is still too strong...')
             54 CALL_FUNCTION            1
"""
"""
 40     >>   18 LOAD_GLOBAL              2 (input)
             20 LOAD_CONST               2 ('What was inside the eye? > ')
             22 CALL_FUNCTION            1
             24 STORE_FAST               0 (answer)

 42          26 LOAD_FAST                0 (answer)
             28 LOAD_GLOBAL              3 (reverse_the_wind)
             30 LOAD_GLOBAL              4 (EYE_DATA)
             32 CALL_FUNCTION            1
             34 COMPARE_OP               2 (==)
             36 POP_JUMP_IF_FALSE       25 (to 50)

 43          38 LOAD_GLOBAL              1 (print)
             40 LOAD_CONST               3 ('The typhoon is gone. Correct!')
"""

answer = server.reverse_the_wind(server.EYE_DATA)
if isinstance(answer, bytes):
    # ① answer が「バイナリデータ（bytes型）」の場合
    sys.stdout.buffer.write(answer)
    
else:
    # ② answer が「通常の文字列（str型）」の場合
    sys.stdout.write(str(answer))

"""
latin1でencode(0x00~0xFFなので)、値を強制的にchar型に変えているため、latin1で数値に直す必要がある
 python3.10 -c "import server; print(server.reverse_the_wind(server.EYE_DATA).encode('latin1').decode('utf-8', errors='ignore'))"

Alpaca{DUMMY}
"""
