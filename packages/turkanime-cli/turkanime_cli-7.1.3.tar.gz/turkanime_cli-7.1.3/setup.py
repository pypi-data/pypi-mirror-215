# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['turkanime_api', 'turkanime_api.cli']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1',
 'easygui>=0.98.2',
 'py7zr',
 'questionary',
 'requests',
 'rich>=9.5.1',
 'selenium>=3.141.0,<4.3.0',
 'youtube_dl>=2021.0.0']

entry_points = \
{'console_scripts': ['turkanime = turkanime_api.cli.turkanime:run']}

setup_kwargs = {
    'name': 'turkanime-cli',
    'version': '7.1.3',
    'description': 'Türkanime video oynatıcı ve indirici',
    'long_description': "# TürkAnimu-Cli\n[![GitHub all releases](https://img.shields.io/github/downloads/kebablord/turkanime-indirici/total?style=flat-square)](https://github.com/KebabLord/turkanime-indirici/releases/latest)  [![GitHub release (latest by date)](https://img.shields.io/github/v/release/kebablord/turkanime-indirici?style=flat-square)](https://github.com/kebablord/turkanime-indirici/releases/latest/download/turkanimu.exe)  [![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/kebablord/turkanime-indirici/.github/workflows/main.yml?style=flat-square)](https://github.com/KebabLord/turkanime-indirici/actions) [![Pypi version](https://img.shields.io/pypi/v/turkanime-cli?style=flat-square)](https://pypi.org/project/turkanime-cli/)\n\nTürkanime için terminal video oynatıcı ve indirici. İtinayla her bölümü indirir & oynatır.\n - Yığın bölüm indirebilir\n - Animu izleyebilir\n - Uygulama içinden arama yapabilir\n - Fansub seçtirebilir\n - Bir yandan izlerken bir yandan animeyi kaydedebilir\n - İndirmelere kaldığı yerden devam edebilir\n \n#### Desteklenen kaynaklar:\n```Sibnet, Odnoklassinki, Sendvid, Mail.ru, VK, Google+, Myvi, GoogleDrive, Yandisk, Vidmoly, Yourupload, Dailymotion```\n\n#### Yenilikler:\n - Seçim ekranı en son seçilen bölümden başlıyor, https://github.com/KebabLord/turkanime-indirici/discussions/35 https://github.com/KebabLord/turkanime-indirici/discussions/30\n - Aynı anda birden fazla bölüm indirme özelliği https://github.com/KebabLord/turkanime-indirici/pull/49\n - Önceden indirilen veya izlenen animelere izlendi ikonu seçeneği\n - Gereksinimleri uygulama içinden otomatik indirme\n\n\n\n# Kurulum\nÖnceden derlenmiş sürümleri [indirebilir](https://github.com/KebabLord/turkanime-indirici/releases/latest) ya da pip ile kolayca `pip install turkanime-cli` kurabilirsiniz. Pip ile kuruyorsanız, ya da scripti kaynak kodundan çalıştırıyorsanız mpv ve geckodriver'ın sisteminizde kurulu olduğundan ve sistem path'ında olduğundan emin olun. Konuya ilişkin rehber için [wiki sayfası](https://github.com/KebabLord/turkanime-indirici/wiki/Herhangi-bir-uygulamay%C4%B1-system-path'%C4%B1na-ekleme).\n\n ### İzleme ekranı\n ![indirme.gif](docs/ss_izle.gif)\n\n ### İndirme ekranı\n ![indirme.gif](docs/ss_indir.gif)\n\n### Yapılacaklar:\n - [ ] İndirme bitimi aksiyonları: bildirim veya bilgisayar kapatma.\n - [ ] Maximum çözünürlüğe ulaş.\n - [ ] Gui versiyon\n - [ ] Youtube-dl yerine yt-dlp'ye geçilmeli.\n - [ ] Selenium'dan kurtulma\n - [x] ~~Yeni sürüm var mı uygulama açılışında kontrol et.~~\n - [x] ~~Paralel anime indirme özelliği.~~\n - [x] ~~Progress yaratılma satırı minimal bir class ile kısaltılacak.~~\n - [x] ~~Domain güncellemesinden beridir kod stabil çalışmıyor, düzeltilecek.~~\n - [x] ~~Kod çorba gibi, basitleştirilecek.~~\n - [x] ~~Navigasyon ve indirme algoritması http talepleriyle sağlanacak.~~\n - [x] ~~Zaman bloğu olarak sleep'den kurtulunacak, elementin yüklenmesi beklenecek.~~\n - [x] ~~Prompt kütüphanesi olarak berbat durumda olan PyInquirer'den Questionary'e geçilecek.~~\n - [x] ~~Arama sonuçları da http talepleriyle getirilecek.~~\n - [x] ~~Fansub seçme özelliği tekrar eklenecek.~~\n",
    'author': 'Junicchi',
    'author_email': 'junicchi@waifu.club',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kebablord/turkanime-indirici',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
