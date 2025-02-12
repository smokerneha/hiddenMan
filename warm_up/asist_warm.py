import asyncio
import random
from dataclasses import dataclass
from telethon import TelegramClient, types
from typing import Optional
from telethon.tl.functions.messages import SendReactionRequest
import time
from typing import List
from telethon.tl.functions.channels import JoinChannelRequest


@dataclass
class WARM_UP:
    client: TelegramClient
    forward_group_link: str
    mes_group_link: str
    private_chatter: List
    limit: int = 200 # limit for mes to iter in group
    send_to_private = False # check before rename to true that private chatter is not blank

    async def like_mes(self, where_to_like: str):
        reactions = ['❤', '🔥', '😭', '⚡', '👍']
        async with self.client:
            reaction = random.choice (reactions)
            group = await self.client.get_entity (where_to_like)
            all_mes = await self.client.get_messages (group, limit=30)
            if len(all_mes) < 2: # ели мало диалогов написать привет
                await self.send_mes(where_to_like, 'hello')
            if len(all_mes) <= 30:
                mes_to_react = all_mes[random.randint (0, len (all_mes) - 1)]
            else:
                mes_to_react = all_mes[random.randint (0, 30)]
            while mes_to_react.action is not None:
                if len (all_mes) <= 30:
                    mes_to_react = all_mes[random.randint (0, len (all_mes) - 1)]
                else:
                    mes_to_react = all_mes[random.randint (0, 30)]
            await self.client (SendReactionRequest (peer=group, msg_id=mes_to_react.id,
                                               reaction=[types.ReactionEmoji (
                                                   emoticon=reaction)]))

    async def send_mes(self, where_to_send: str, mes_to_send: str):
        async with self.client:
            group = await self.client.get_entity (where_to_send)
            await self.client.send_message(group, mes_to_send)


    async def get_mes_from_chat(self) -> str:  # return random text mes from group
        async with self.client:
            group = await self.client.get_entity(self.forward_group_link)
            mes = await self.client.get_messages(group, limit=self.limit)
            mes_to_return = mes[random.randint(0, self.limit)]
            while (mes_to_return.action is not None) or (mes_to_return.text == ''):
                mes_to_return = mes[random.randint(0, self.limit)]
            return mes_to_return.text


    async def join_group(self, group_link) -> bool:
        if not (group_link.startswith ('https://t.me/')):
            group_link = 'https://t.me/' + group_link
        async with self.client:
            try:
                group = await self.client.get_entity (group_link)
                await self.client (JoinChannelRequest (group))
                name = await self.client.get_entity ('me')
                print (f'{name.first_name} successfully joined {group_link}')
                return True
            except Exception as err:
                if err is ValueError:
                    print ("group with this username doesn't seem to exist")
                    return False
                else:
                    print (f'Something went wrong {err}')
                    return False

    async def start(self, time_to_run_sec):
        # join both groups
        try:
            await self.join_group (self.forward_group_link)
            await self.join_group(self.mes_group_link)
        except Exception as err:
            return False, f'Something wrong with group links {err}'

        # del ur username from list
        async with self.client:
            me = await self.client.get_me()
            username = me.username

        self.private_chatter.remove(str(username))

        # first mes - always hello there
        first_mes = ['Hello there', 'morning', 'Hi', 'Hi there', 'Hey', 'hello guys', 'Howdy', 'helloooooo', 'Hello again']

        # в цикле ждать сколько-то рандомно потом слать сообщение или лайкать рандомно
        like_or_send = random.randint(0, 100) # if 0, 34 - send mes, 35 - 100 like - 34% mes, 66% like
        private_or_chat = random.randint(0, 100) # 30 - private 70 chat
        start = time.time()
        stop = 0
        await self.send_mes(self.mes_group_link, first_mes[random.randint(0, len(first_mes) -1)])
        while stop <= time_to_run_sec:
            if self.send_to_private is False:
                like_or_send = random.randint (0, 100)
                if like_or_send <= 34: # send mes to group
                    mes_to_send = await self.get_mes_from_chat()
                    await self.send_mes(self.mes_group_link, mes_to_send)
                else:
                    await self.like_mes(self.mes_group_link) # like mes in group

            elif self.send_to_private:
                private_or_chat = random.randint (0, 100)
                like_or_send = random.randint (0, 100)

                # sending private and group messages
                if like_or_send <= 34 and private_or_chat <= 30: # send private mes
                    mes_to_send = await self.get_mes_from_chat ()
                    await self.send_mes (self.private_chatter[random.randint(0, len(self.private_chatter)-1 )], mes_to_send) # choose random user from list and send message
                elif like_or_send <= 34 and private_or_chat >= 31: # send chat message
                    mes_to_send = await self.get_mes_from_chat()
                    await self.send_mes(self.mes_group_link, mes_to_send)

                # like in private or in group
                elif like_or_send >= 35 and private_or_chat >= 31: # send chat like
                    await self.like_mes(self.mes_group_link)
                elif like_or_send >= 35 and private_or_chat <= 30:
                    await self.like_mes(self.private_chatter[random.randint(0, len(self.private_chatter)-1 )])
            # sleep 20 - 120 min after sending for 20 min
            stop = time.time () - start
            need_sleep = 1200
            sleeping_time = random.randint(1200, 7200)
            if  stop > need_sleep:
                await asyncio.sleep(sleeping_time)
                need_sleep += sleeping_time
                need_sleep += random.randint(1200, 2300)
            else:
                await asyncio.sleep (random.randint (55, 120)) # sleep after action











