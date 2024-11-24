from requests import get,post,patch,delete

# response = post(
#     "http://127.0.0.1:8000/user/",
#     json={"login":"pavel223", "password":"12hh345"},
#     headers={"header":'admin'})

# print(response.status_code)
# print(response.text)
# # Работает

# response = post(
#     "http://127.0.0.1:8000/user/login/",
#     json={"login":"pavel223", "password":"12hh345"})

# print(response.status_code)
# print(response.text)
# # Работает

# response = get(
#     "http://127.0.0.1:8000/user/1/")

# print(response.status_code)
# print(response.text)
# # Работает

# response = patch(
#     "http://127.0.0.1:8000/user/1/",
#     json={"login":"pavel223", "password":"12hh345",
#         "new_login":"pavel2231", "new_password":"12hh3451"},)

# print(response.status_code)
# print(response.text)
# # Работает

# response = delete(
#     "http://127.0.0.1:8000/user/1/",
#     json={"login":"pavel2231", "password":"12hh3451"})

# print(response.status_code)
# print(response.text)
# Работает


# response = post(
#     "http://127.0.0.1:8000/advertisement/",
#     json={"title" : "Заголовок",
#     "description" : "описание всего" ,
#     "price" : 399.111,
#     "author" : "Пушкин"},
#     headers={"token":'07ac3557-9f37-49f8-ac07-d838f43d4ecb'}) ##Токен строка 12

# print(response.status_code)
# print(response.text)
## Работает

# response = patch(
#     "http://127.0.0.1:8000/advertisement/1/",
#     json={"title" : "новый Заголовок",
#     "description" : "новое описание" },
#     headers={"token":'07ac3557-9f37-49f8-ac07-d838f43d4ecb'}) ##Токен строка 12

# print(response.status_code)
# print(response.text)
## Работает

# response = delete(
#     "http://127.0.0.1:8000/advertisement/1/",
#     headers={"token":'07ac3557-9f37-49f8-ac07-d838f43d4ecb'}) ##Токен строка 12

# print(response.status_code)
# print(response.text)
# ## Работает


# response = get(
#     "http://127.0.0.1:8000/advertisement/2/")

# print(response.status_code)
# print(response.text)
## Работает

