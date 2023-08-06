# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiogram3_form']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aiogram3-form',
    'version': '0.5.1',
    'description': 'A library to create forms in aiogram3',
    'long_description': '# aiogram3-form\nA library to create forms in aiogram3\n\n```shell\npip install aiogram3-form\n```\n\n# Example\n```Python\nimport asyncio\n\nfrom aiogram import Bot, Dispatcher, F, Router, types\nfrom aiogram3_form import Form, FormField\nfrom aiogram.fsm.context import FSMContext\n\nbot = Bot(token=YOUR_TOKEN)\ndispatcher = Dispatcher()\nrouter = Router()\ndispatcher.include_router(router)\n\n\nclass NameForm(Form, router=router):\n    first_name: str = FormField(enter_message_text="Enter your first name please")\n    second_name: str = FormField(\n        enter_message_text="Enter your second name please",\n        filter=F.text.len() > 10 & F.text,\n    )\n    age: int = FormField(\n        enter_message_text="Enter age as integer",\n        error_message_text="Age should be numeric!",\n    )\n\n\n@NameForm.submit()\nasync def name_form_submit_handler(form: NameForm, event_chat: types.Chat):\n    # handle form data\n    # also supports aiogram standart DI (e. g. middlewares, filters, etc)\n    await form.answer(\n        f"{form.first_name} {form.second_name} of age {form.age} in chat {event_chat.title}"\n    )\n\n\n@router.message(F.text == "/form")\nasync def form_handler(_, state: FSMContext):\n    await NameForm.start(bot, state)  # start your form\n\n\nasync def main():\n    await dispatcher.start_polling(bot)\n\n\nasyncio.run(main())\n```\n',
    'author': 'TrixiS',
    'author_email': 'oficialmorozov@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
