# Receipts parser

## API example

```
import requests

url = 'http://0.0.0.0:9000/process_image'
my_image = {'image': open('1.jpg', mode='rb')}

requests.post(url=url, files=my_image).json()
```

Result:
```
{
    "date": "01.12.2020 21:03,
    "products": [
        {
            "category": "Другое; Другое",
            "full_name": "Пирог праздничный a чак",
            "price": 0.38
        },
        {
            "category": "Продукты питания; Хлеб и хлебобулочные изделия",
            "full_name": "Хлеб бездрожжевой бабушкин",
            "price": 0.87
        },
        {
            "category": "Продукты питания; Кондитерские изделия",
            "full_name": "Вафли ранет",
            "price": 0.0
        }
    ],
    "shop": "Виталюр
}
```
