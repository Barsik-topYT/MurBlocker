import sys
import os

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

import i18n
import time
import ctypes
import winreg
import subprocess
import shutil
import re
from datetime import datetime
from urllib.parse import urlparse
from colorama import init, Fore, Back, Style

# Языковые настройки
LANGUAGES = {
    'ru': {   
        'title': "БЛОКИРОВЩИК ПРОГРАММ 1.5",
        'by': "by BarsikYT",
        'admin_rights': "Программа запущена с правами администратора",
        'reboot_required': "ВАЖНО: Для работы блокировок сайтов, требуется выключить VPN. (Он обходит данные блокировки)",
        'menu_title': "ГЛАВНОЕ МЕНЮ:",
        'menu_items': [
            "Блокировка программ",
            "Блокировка сайтов", 
            "Разблокировать все программы",
            "Разблокировать все сайты",
            "Просмотр текущих блокировок",
            "Тестирование блокировки",
            "Обновить политики (применить изменения)",
            "Сменить язык / Change language",
            "Выход"
        ],
        'select_program': "Выберите программу для блокировки:",
        'select_site_category': "Выберите категорию сайтов для блокировки:",
        'block_program': "Блокировка {}...",
        'block_websites': "Блокировка сайтов...",
        'unblock_all_programs': "Разблокировка всех программ...",
        'unblock_all_websites': "Разблокировка всех сайтов...",
        'current_blocks': "Текущие блокировки:",
        'testing_block': "Тестирование блокировки...",
        'refresh_policies': "Обновление политик...",
        'choice': "Ваш выбор:",
        'continue_confirm': "Продолжить? (y/n):",
        'reboot_confirm': "Перезагрузить компьютер? (y/n):",
        'unblock_confirm': "Вы уверены, что хотите разблокировать все программы? (y/n):",
        'unblock_sites_confirm': "Вы уверены, что хотите разблокировать все сайты? (y/n):",
        'enter_to_continue': "Нажмите Enter для продолжения...",
        'exiting': "Завершение работы...",
        'invalid_choice': "Неверный выбор",
        'no_programs': "Нет блокировок",
        'no_sites': "Нет заблокированных сайтов",
        'policy_status': "Политика DisallowRun:",
        'enabled': "ВКЛЮЧЕНА",
        'disabled': "ВЫКЛЮЧЕНА",
        'not_configured': "НЕ НАСТРОЕНА",
        'total_program_blocks': "Всего активных блокировок программ:",
        'total_site_blocks': "Всего заблокированных сайтов:",
        'programs': {
            '1': "БРАУЗЕР YANDEX",
            '2': "БРАУЗЕР OPERA", 
            '3': "AVAST",
            '4': "360 TOTAL SECURITY",
            '5': "uTORRENT",
            '6': "CCLEANER",
            '7': "ONEDRIVE",
            '8': "MAX",
            '9': "MEDIAGET",
            'ALL': "ЗАПРЕТИТЬ ВСЁ"
        },
        'sites': {
            '1': "ЯНДЕКС",
            '2': "Mail.ru",
            '3': "UTORRENT", 
            '4': "MAX"
        },
        'site_blocking': "БЛОКИРОВКА САЙТОВ",
        'enter_sites': "Введите сайты для блокировки (через запятую или каждый с новой строки)",
        'site_example': "Пример: yandex.ru или https://dzen.ru/ (не только URL в браузере)",
        'finish_enter': "Для завершения ввода введите пустую строку",
        'enter_site': "Введите сайт (или Enter для завершения):",
        'will_block': "Будут заблокированы:",
        'sites_blocked': "Сайты успешно заблокированы!",
        'browser_restart': "Закройте браузер полностью. Отключите «Защищённый DNS» вручную, если он снова включится.",
        'no_sites_entered': "Не введено ни одного сайта",
        'site_options': "Блокировка сайтов:",
        'site_choices': [
            "Выбрать из списка",
            "Ввести вручную"
        ],
        'blocked_sites': "Заблокированные сайты:",
        'select_language': "Выберите язык / Select language:",
        'language_changed': "Язык изменен на русский",
        'gui': {
            'window_title': "MurBlocker 1.5",
            'subtitle': "Блокировщик программ и сайтов",
            'nav_programs': "Программы",
            'nav_sites': "Сайты",
            'nav_status': "Статус",
            'nav_tools': "Инструменты",
            'block_btn': "Заблокировать",
            'block_all_btn': "Заблокировать всё",
            'unblock_programs': "Разблокировать все программы",
            'unblock_sites': "Разблокировать все сайты",
            'refresh_policies_btn': "Обновить политики",
            'flush_dns_btn': "Очистить DNS",
            'custom_site_label': "Свой домен (например vk.com):",
            'custom_site_block': "Добавить в блокировку",
            'presets_title': "Готовые наборы",
            'log_title': "Журнал операций",
            'admin_ok': "Администратор",
            'no_admin': "Нет прав администратора",
            'confirm': "Подтверждение",
            'confirm_block_prog': "Заблокировать «{}»?",
            'confirm_unblock_prog': "Разблокировать все программы?",
            'confirm_unblock_sites': "Разблокировать все сайты?",
            'confirm_reboot': "Перезагрузить компьютер сейчас?",
            'done': "Готово",
            'error': "Ошибка",
            'blocked_programs': "Заблокированные программы",
            'blocked_sites': "Заблокированные сайты",
            'policy_label': "Политика DisallowRun:",
            'language': "Язык",
            'exit': "Выход",
            'manual_sites_hint': "Несколько доменов через запятую",
            'version_label': "Версия 1.5",
            'lang_changed': "Язык интерфейса обновлён.",
        },
    },
    'en': {
        'title': "PROGRAM BLOCKER 1.5", 
        'by': "by BarsikYT",
        'admin_rights': "Program running with administrator rights",
        'reboot_required': "IMPORTANT: Reboot required for blocking to work!",
        'menu_title': "MAIN MENU:",
        'menu_items': [
            "Block programs",
            "Block websites",
            "Unblock all programs", 
            "Unblock all websites",
            "View current blocks",
            "Test blocking",
            "Refresh policies (apply changes)",
            "Change language / Сменить язык",
            "Exit"
        ],
        'select_program': "Select program to block:",
        'select_site_category': "Select website category to block:",
        'block_program': "Blocking {}...",
        'block_websites': "Blocking websites...",
        'unblock_all_programs': "Unblocking all programs...",
        'unblock_all_websites': "Unblocking all websites...",
        'current_blocks': "Current blocks:",
        'testing_block': "Testing blocking...",
        'refresh_policies': "Refreshing policies...",
        'choice': "Your choice:",
        'continue_confirm': "Continue? (y/n):",
        'reboot_confirm': "Reboot computer? (y/n):",
        'unblock_confirm': "Are you sure you want to unblock all programs? (y/n):",
        'unblock_sites_confirm': "Are you sure you want to unblock all websites? (y/n):",
        'enter_to_continue': "Press Enter to continue...",
        'exiting': "Exiting...",
        'invalid_choice': "Invalid choice",
        'no_programs': "No blocks",
        'no_sites': "No blocked websites",
        'policy_status': "DisallowRun policy:",
        'enabled': "ENABLED",
        'disabled': "DISABLED", 
        'not_configured': "NOT CONFIGURED",
        'total_program_blocks': "Total active program blocks:",
        'total_site_blocks': "Total blocked websites:",
        'programs': {
            '1': "YANDEX BROWSER",
            '2': "OPERA BROWSER",
            '3': "AVAST", 
            '4': "360 TOTAL SECURITY",
            '5': "UTORRENT",
            '6': "CCLEANER",
            '7': "ONEDRIVE",
            '8': "MAX",
            '9': "MEDIAGET",
            'ALL': "BLOCK EVERYTHING"
        },
        'sites': {
            '1': "YANDEX",
            '2': "Mail.ru",
            '3': "UTORRENT",
            '4': "MAX"
        },
        'site_blocking': "WEBSITE BLOCKING",
        'enter_sites': "Enter websites to block (comma separated or one per line)",
        'site_example': "Example: yandex.ru, dzen.ru, vk.com",
        'finish_enter': "Enter empty line to finish",
        'enter_site': "Enter website (or Enter to finish):",
        'will_block': "Will be blocked:",
        'sites_blocked': "Websites successfully blocked!",
        'browser_restart': "Browser restart may be required for changes to take effect",
        'no_sites_entered': "No websites entered",
        'site_options': "Website blocking:",
        'site_choices': [
            "Select from list",
            "Enter manually"
        ],
        'blocked_sites': "Blocked websites:",
        'select_language': "Select language / Выберите язык:",
        'language_changed': "Language changed to English",
        'gui': {
            'window_title': "MurBlocker 1.5",
            'subtitle': "Program & website blocker",
            'nav_programs': "Programs",
            'nav_sites': "Websites",
            'nav_status': "Status",
            'nav_tools': "Tools",
            'block_btn': "Block",
            'block_all_btn': "Block all",
            'unblock_programs': "Unblock all programs",
            'unblock_sites': "Unblock all websites",
            'refresh_policies_btn': "Refresh policies",
            'flush_dns_btn': "Flush DNS",
            'custom_site_label': "Custom domain (e.g. vk.com):",
            'custom_site_block': "Add to block list",
            'presets_title': "Presets",
            'log_title': "Activity log",
            'admin_ok': "Administrator",
            'no_admin': "No admin rights",
            'confirm': "Confirm",
            'confirm_block_prog': "Block «{}»?",
            'confirm_unblock_prog': "Unblock all programs?",
            'confirm_unblock_sites': "Unblock all websites?",
            'confirm_reboot': "Reboot computer now?",
            'done': "Done",
            'error': "Error",
            'blocked_programs': "Blocked programs",
            'blocked_sites': "Blocked websites",
            'policy_label': "DisallowRun policy:",
            'language': "Language",
            'exit': "Exit",
            'manual_sites_hint': "Multiple domains separated by commas",
            'version_label': "Version 1.5",
            'lang_changed': "Interface language updated.",
        },
    },
    'zh': {
        'title': "程序拦截器 1.5",
        'by': "by BarsikYT",
        'admin_rights': "程序以管理员权限运行",
        'reboot_required': "重要：拦截功能需要重启才能生效！",
        'menu_title': "主菜单：",
        'menu_items': [
            "拦截程序",
            "拦截网站",
            "解除所有程序拦截",
            "解除所有网站拦截",
            "查看当前拦截",
            "测试拦截功能",
            "刷新策略（应用更改）",
            "切换语言",
            "退出"
        ],
        'select_program': "选择要拦截的程序：",
        'select_site_category': "选择要拦截的网站类别：",
        'block_program': "正在拦截 {}...",
        'block_websites': "正在拦截网站...",
        'unblock_all_programs': "正在解除所有程序拦截...",
        'unblock_all_websites': "正在解除所有网站拦截...",
        'current_blocks': "当前拦截：",
        'testing_block': "正在测试拦截...",
        'refresh_policies': "正在刷新策略...",
        'choice': "您的选择：",
        'continue_confirm': "继续？(y/n)：",
        'reboot_confirm': "重启计算机？(y/n)：",
        'unblock_confirm': "确定要解除所有程序拦截吗？(y/n)：",
        'unblock_sites_confirm': "确定要解除所有网站拦截吗？(y/n)：",
        'enter_to_continue': "按Enter键继续...",
        'exiting': "正在退出...",
        'invalid_choice': "无效选择",
        'no_programs': "无拦截",
        'no_sites': "无被拦截网站",
        'policy_status': "DisallowRun策略：",
        'enabled': "已启用",
        'disabled': "已禁用",
        'not_configured': "未配置",
        'total_program_blocks': "活动程序拦截总数：",
        'total_site_blocks': "被拦截网站总数：",
        'programs': {
            '1': "YANDEX浏览器",
            '2': "OPERA浏览器",
            '3': "AVAST",
            '4': "360安全卫士",
            '5': "UTORRENT",
            '6': "CCLEANER",
            '7': "ONEDRIVE",
            '8': "MAX",
            '9': "MEDIAGET",
            'ALL': "拦截所有程序"
        },
        'sites': {
            '1': "YANDEX",
            '2': "Mail.ru",
            '3': "UTORRENT",
            '4': "MAX"
        },
        'site_blocking': "网站拦截",
        'enter_sites': "输入要拦截的网站（用逗号分隔或每行一个）",
        'site_example': "示例：yandex.ru, dzen.ru, vk.com",
        'finish_enter': "输入空行完成",
        'enter_site': "输入网站（或按Enter完成）：",
        'will_block': "将拦截：",
        'sites_blocked': "网站成功被拦截！",
        'browser_restart': "更改生效可能需要重启浏览器",
        'no_sites_entered': "未输入任何网站",
        'site_options': "网站拦截：",
        'site_choices': [
            "从列表选择",
            "手动输入"
        ],
        'blocked_sites': "被拦截的网站：",
        'select_language': "选择语言：",
        'language_changed': "语言已切换为中文"
    },
    'de': {
        'title': "PROGRAMM-BLOCKER 1.5",
        'by': "by BarsikYT",
        'admin_rights': "Programm wird mit Administratorrechten ausgeführt",
        'reboot_required': "WICHTIG: Neustart erforderlich, damit Blockierungen funktionieren!",
        'menu_title': "HAUPTMENÜ:",
        'menu_items': [
            "Programme blockieren",
            "Websites blockieren",
            "Alle Programme freischalten",
            "Alle Websites freischalten",
            "Aktuelle Blockierungen anzeigen",
            "Blockierung testen",
            "Richtlinien aktualisieren (Änderungen anwenden)",
            "Sprache ändern",
            "Beenden"
        ],
        'select_program': "Wählen Sie ein Programm zum Blockieren:",
        'select_site_category': "Wählen Sie eine Website-Kategorie zum Blockieren:",
        'block_program': "Blockiere {}...",
        'block_websites': "Blockiere Websites...",
        'unblock_all_programs': "Gebe alle Programme frei...",
        'unblock_all_websites': "Gebe alle Websites frei...",
        'current_blocks': "Aktuelle Blockierungen:",
        'testing_block': "Teste Blockierung...",
        'refresh_policies': "Aktualisiere Richtlinien...",
        'choice': "Ihre Auswahl:",
        'continue_confirm': "Fortfahren? (j/n):",
        'reboot_confirm': "Computer neu starten? (j/n):",
        'unblock_confirm': "Sind Sie sicher, dass Sie alle Programme freischalten möchten? (j/n):",
        'unblock_sites_confirm': "Sind Sie sicher, dass Sie alle Websites freischalten möchten? (j/n):",
        'enter_to_continue': "Drücken Sie Enter zum Fortfahren...",
        'exiting': "Beende...",
        'invalid_choice': "Ungültige Auswahl",
        'no_programs': "Keine Blockierungen",
        'no_sites': "Keine blockierten Websites",
        'policy_status': "DisallowRun-Richtlinie:",
        'enabled': "AKTIVIERT",
        'disabled': "DEAKTIVIERT",
        'not_configured': "NICHT KONFIGURIERT",
        'total_program_blocks': "Gesamte aktive Programmblockierungen:",
        'total_site_blocks': "Gesamte blockierte Websites:",
        'programs': {
            '1': "YANDEX BROWSER",
            '2': "OPERA BROWSER",
            '3': "AVAST",
            '4': "360 TOTAL SECURITY",
            '5': "UTORRENT",
            '6': "CCLEANER",
            '7': "ONEDRIVE",
            '8': "MAX",
            '9': "MEDIAGET",
            'ALL': "ALLE BLOCKIEREN"
        },
        'sites': {
            '1': "YANDEX",
            '2': "Mail.ru",
            '3': "UTORRENT",
            '4': "MAX"
        },
        'site_blocking': "WEBSITE-BLOCKIERUNG",
        'enter_sites': "Geben Sie zu blockierende Websites ein (durch Kommas getrennt oder eine pro Zeile)",
        'site_example': "Beispiel: yandex.ru, dzen.ru, vk.com",
        'finish_enter': "Leere Zeile eingeben zum Beenden",
        'enter_site': "Website eingeben (oder Enter zum Beenden):",
        'will_block': "Wird blockiert:",
        'sites_blocked': "Websites erfolgreich blockiert!",
        'browser_restart': "Browser-Neustart möglicherweise erforderlich, damit Änderungen wirksam werden",
        'no_sites_entered': "Keine Websites eingegeben",
        'site_options': "Website-Blockierung:",
        'site_choices': [
            "Aus Liste auswählen",
            "Manuell eingeben"
        ],
        'blocked_sites': "Blockierte Websites:",
        'select_language': "Sprache auswählen:",
        'language_changed': "Sprache auf Deutsch geändert"
    }
}

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
HOSTS_BACKUP_PATH = r"C:\Windows\System32\drivers\etc\hosts.backup"
BLOCKER_HEADER = "# === BLOCKED BY BARSIKYT BLOCKER ==="
FIREWALL_RULE_PREFIX = "MurBlocker"

# Официальные подсети Яндекса (AS13238, документация Yandex 360)
YANDEX_IP_CIDRS_V4 = [
    "5.45.192.0/18", "5.255.192.0/18", "37.9.64.0/18", "37.9.82.144/28", "37.9.102.64/28",
    "37.140.128.0/18", "77.88.0.0/18", "77.88.7.48/28", "84.252.160.0/19", "87.250.224.0/19",
    "90.156.176.0/22", "93.158.128.0/18", "95.108.128.0/17", "141.8.128.0/18",
    "178.154.128.0/18", "185.32.187.0/24", "185.206.164.0/22", "213.180.192.0/19",
]
YANDEX_IP_CIDRS_V6 = [
    "2a02:6b8::/32", "2a02:6b8:0:2001::/64", "2a02:6b8:0:1a0b::/64", "2a02:6b8:11d:c::/64",
]

YANDEX_BLOCK_DOMAINS = [
    "yandex.ru", "ya.ru", "yandex.com", "yandex.net", "yandex.by", "yandex.kz", "yandex.uz",
    "yandex.st", "yandex-team.ru", "dzen.ru", "yastatic.net", "yandexadexchange.net",
    "passport.yandex.ru", "mail.yandex.ru", "disk.yandex.ru", "music.yandex.ru",
    "metrika.yandex.ru", "mc.yandex.ru", "api.browser.yandex.ru", "browser.yandex.ru",
    "download.yandex.ru", "update.browser.yandex.ru", "cdn.yandex.net", "cdn.yandex.ru",
    "strm.yandex.ru", "an.yandex.ru", "avatars.mds.yandex.net", "cloud-api.yandex.net",
    "oauth.yandex.ru", "translate.yandex.net", "messenger.yandex.ru", "telemost.yandex.ru",
    "backend.messenger.yandex.ru", "files.messenger.yandex.ru", "goloom.strm.yandex.net",
    "stun.rtc.yandex.net", "turn.webrtc.yandex.net", "push.yandex.ru", "calendar.yandex.ru",
    "docs.yandex.ru", "alice.yandex.ru", "tv.yandex.ru", "market.yandex.ru",
    "maps.yandex.ru", "l7test.yandex.ru", "suggest.yandex.ru", "clck.yandex.ru",
]

DOH_BLOCK_DOMAINS = [
    "dns.google", "dns.google.com", "dns64.dns.google",
    "cloudflare-dns.com", "one.one.one.one", "security.cloudflare-dns.com", "mozilla.cloudflare-dns.com",
    "dns.quad9.net", "dns.nextdns.io", "doh.opendns.com", "doh.cleanbrowsing.org",
    "dns.adguard.com", "dns.adguard-dns.com", "common.dot.dns.yandex.net",
    "chrome.cloudflare-dns.com", "dns.cloudflare.com",
]

init(autoreset=True)

def t(key):
    """Функция для перевода текста"""
    return LANGUAGES[i18n.get_language()].get(key, key)

def confirm_yes(answer):
    """Проверяет ответ пользователя как согласие (y/да/j и т.д.)"""
    return answer.lower().strip() in ('y', 'j', 'yes', 'да', 'д', 'ja')

def read_hosts_file():
    """Читает hosts с учётом кодировки Windows"""
    for encoding in ('utf-8-sig', 'utf-8', 'cp1251', 'latin-1'):
        try:
            with open(HOSTS_PATH, 'r', encoding=encoding) as f:
                return f.read(), encoding
        except UnicodeDecodeError:
            continue
    with open(HOSTS_PATH, 'r', encoding='utf-8', errors='replace') as f:
        return f.read(), 'utf-8'

def normalize_site(site):
    """Из URL, домена с путём или www. извлекает имя хоста для hosts"""
    site = (site or "").strip()
    if not site:
        return None

    if '://' in site or site.startswith('//'):
        parsed = urlparse(site if '://' in site else 'https:' + site.lstrip('/'))
        host = parsed.hostname
    else:
        chunk = site.split('/')[0].split('?')[0].split('#')[0].strip()
        if '@' in chunk:
            chunk = chunk.split('@')[-1]
        if ':' in chunk:
            host_part, port_part = chunk.rsplit(':', 1)
            if port_part.isdigit():
                chunk = host_part
        host = chunk

    if not host:
        return None

    host = host.lower().rstrip('.')
    if not host or ' ' in host or '/' in host:
        return None
    if not re.match(r'^[a-z0-9]([a-z0-9\-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9\-]*[a-z0-9])?)+$', host):
        return None
    if host.startswith('www.'):
        host = host[4:]
    return host

def site_blocked_in_hosts(content, site):
    """Проверяет, есть ли уже блокировка домена в hosts"""
    site = normalize_site(site) or site.strip().lower()
    if not site:
        return True
    for line in content.splitlines():
        line = line.strip().lower()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[0] in ('127.0.0.1', '0.0.0.0', '::1'):
            if parts[1] == site or parts[1].endswith('.' + site):
                return True
    return False

def expand_site_entries(site):
    """Добавляет www-вариант для полноты блокировки"""
    host = normalize_site(site)
    if not host:
        return []
    entries = [host]
    entries.append('www.' + host)
    return entries

def print_invalid_site(raw):
    if i18n.get_language() == 'ru':
        print(f"⚠ Не удалось распознать сайт: {raw!r} (введите домен, например vk.com)")
    elif i18n.get_language() == 'en':
        print(f"⚠ Could not parse site: {raw!r} (use a domain like vk.com)")
    elif i18n.get_language() == 'zh':
        print(f"⚠ 无法识别网站：{raw!r}（请输入域名，如 vk.com）")
    else:
        print(f"⚠ Seite nicht erkannt: {raw!r} (Domain eingeben, z.B. vk.com)")

def is_admin():
    """Проверяет, запущена ли программа от имени администратора"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def _is_gui_mode():
    return "--cli" not in sys.argv and "-c" not in sys.argv


def run_as_admin(gui=None):
    """Перезапускает программу с правами администратора"""
    if is_admin():
        return True

    if gui is None:
        gui = _is_gui_mode()

    from gui_utils import run_as_admin_elevate, show_admin_message

    if gui:
        admin_msgs = {
            'ru': 'Требуются права администратора.\nПодтвердите запрос UAC.',
            'en': 'Administrator rights required.\nPlease confirm the UAC prompt.',
            'zh': '需要管理员权限。\n请确认 UAC 请求。',
            'de': 'Administratorrechte erforderlich.\nBitte bestätigen Sie die UAC-Abfrage.',
        }
        show_admin_message("MurBlocker", admin_msgs.get(i18n.get_language(), admin_msgs['en']))
        run_as_admin_elevate(gui=True)
    else:
        if i18n.get_language() == 'ru':
            print("Программа требует права администратора...")
        elif i18n.get_language() == 'en':
            print("Program requires administrator rights...")
        elif i18n.get_language() == 'zh':
            print("程序需要管理员权限...")
        else:
            print("Programm erfordert Administratorrechte...")
        time.sleep(2)
        try:
            run_as_admin_elevate(gui=False)
        except Exception as e:
            if i18n.get_language() == 'ru':
                print(f"Ошибка при запросе прав администратора: {e}")
                input("Нажмите Enter для выхода...")
            elif i18n.get_language() == 'en':
                print(f"Error requesting admin rights: {e}")
                input("Press Enter to exit...")
            else:
                print(f"Error: {e}")
                input("Press Enter to exit...")
        sys.exit(0)

def reboot_computer():
    """Выполняет перезагрузку компьютера"""
    print("\n" + "="*50)
    if i18n.get_language() == 'ru':
        print(" ПЕРЕЗАГРУЗКА КОМПЬЮТЕРА")
        print("Компьютер будет перезагружен через 10 секунд...")
        print("Сохраните все важные данные!")
    elif i18n.get_language() == 'en':
        print(" COMPUTER REBOOT")
        print("Computer will reboot in 10 seconds...")
        print("Save all important data!")
    elif i18n.get_language() == 'zh':
        print(" 计算机重启")
        print("计算机将在10秒后重启...")
        print("请保存所有重要数据！")
    else:
        print(" COMPUTER-NEUSTART")
        print("Computer wird in 10 Sekunden neu gestartet...")
        print("Speichern Sie alle wichtigen Daten!")
    print("="*50)
    
    for i in range(10, 0, -1):
        if i18n.get_language() == 'ru':
            print(f"Перезагрузка через: {i} секунд...", end='\r')
        elif i18n.get_language() == 'en':
            print(f"Reboot in: {i} seconds...", end='\r')
        elif i18n.get_language() == 'zh':
            print(f"重启倒计时：{i}秒...", end='\r')
        else:
            print(f"Neustart in: {i} Sekunden...", end='\r')
        time.sleep(1)
    
    if i18n.get_language() == 'ru':
        print("Выполняется перезагрузка...")
    elif i18n.get_language() == 'en':
        print("Rebooting...")
    elif i18n.get_language() == 'zh':
        print("正在重启...")
    else:
        print("Starte neu...")
    try:
        os.system("shutdown /r /t 0")
    except Exception as e:
        if i18n.get_language() == 'ru':
            print(f"Ошибка при перезагрузке: {e}")
        elif i18n.get_language() == 'en':
            print(f"Reboot error: {e}")
        elif i18n.get_language() == 'zh':
            print(f"重启时出错：{e}")
        else:
            print(f"Fehler beim Neustart: {e}")

def ask_reboot():
    """Спрашивает пользователя о перезагрузке"""
    print("\n" + "="*50)
    if i18n.get_language() == 'ru':
        print(" ДЛЯ ПРИМЕНЕНИЯ ИЗМЕНЕНИЙ ТРЕБУЕТСЯ ПЕРЕЗАГРУЗКА")
        print("Блокировка будет работать только после перезагрузки!")
        print("Выберите действие:")
        print("1. Перезагрузить сейчас (y)")
        print("2. Перезагрузить позже (n)")
    elif i18n.get_language() == 'en':
        print(" REBOOT REQUIRED FOR CHANGES TO TAKE EFFECT")
        print("Blocking will only work after reboot!")
        print("Choose action:")
        print("1. Reboot now (y)")
        print("2. Reboot later (n)")
    elif i18n.get_language() == 'zh':
        print(" 需要重启以使更改生效")
        print("拦截功能只有在重启后才能工作！")
        print("选择操作：")
        print("1. 立即重启 (y)")
        print("2. 稍后重启 (n)")
    else:
        print(" NEUSTART ERFORDERLICH FÜR ÄNDERUNGEN")
        print("Blockierung funktioniert nur nach Neustart!")
        print("Aktion wählen:")
        print("1. Jetzt neu starten (j)")
        print("2. Später neu starten (n)")
    print("="*50)
    
    while True:
        choice = input(t('reboot_confirm')).lower().strip()
        if choice in ['y', 'н', 'да', 'yes', 'j']:
            return True
        elif choice in ['n', 'т', 'нет', 'no']:
            return False
        else:
            if i18n.get_language() == 'ru':
                print("Пожалуйста, введите 'y' (да) или 'n' (нет)")
            elif i18n.get_language() == 'en':
                print("Please enter 'y' (yes) or 'n' (no)")
            elif i18n.get_language() == 'zh':
                print("请输入 'y' (是) 或 'n' (否)")
            else:
                print("Bitte geben Sie 'j' (ja) oder 'n' (nein) ein")

def refresh_policy():
    """Обновляет групповые политики для применения изменений"""
    try:
        print(t('refresh_policies'))
        result = subprocess.run(['gpupdate', '/force'], capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            if i18n.get_language() == 'ru':
                print("✓ Политики обновлены")
            elif i18n.get_language() == 'en':
                print("✓ Policies updated")
            elif i18n.get_language() == 'zh':
                print("✓ 策略已更新")
            else:
                print("✓ Richtlinien aktualisiert")
        else:
            if i18n.get_language() == 'ru':
                print("⚠ gpupdate завершился с ошибкой, пробуем альтернативный метод...")
            elif i18n.get_language() == 'en':
                print("⚠ gpupdate failed, trying alternative method...")
            elif i18n.get_language() == 'zh':
                print("⚠ gpupdate失败，尝试替代方法...")
            else:
                print("⚠ gpupdate fehlgeschlagen, versuche alternative Methode...")
            subprocess.run(['taskkill', '/f', '/im', 'explorer.exe'], capture_output=True)
            time.sleep(2)
            subprocess.Popen('explorer.exe')
            if i18n.get_language() == 'ru':
                print("✓ Проводник перезапущен")
            elif i18n.get_language() == 'en':
                print("✓ Explorer restarted")
            elif i18n.get_language() == 'zh':
                print("✓ 资源管理器已重启")
            else:
                print("✓ Explorer neu gestartet")
        return True
    except Exception as e:
        if i18n.get_language() == 'ru':
            print(f"⚠ Ошибка обновления политик: {e}")
        elif i18n.get_language() == 'en':
            print(f"⚠ Policy update error: {e}")
        elif i18n.get_language() == 'zh':
            print(f"⚠ 策略更新错误：{e}")
        else:
            print(f"⚠ Richtlinienaktualisierungsfehler: {e}")
        return False

def flush_dns():
    """Очищает кэш DNS"""
    try:
        if i18n.get_language() == 'ru':
            print("Очистка кэша DNS...")
        elif i18n.get_language() == 'en':
            print("Flushing DNS cache...")
        elif i18n.get_language() == 'zh':
            print("正在清除DNS缓存...")
        else:
            print("Leere DNS-Cache...")
        subprocess.run(['ipconfig', '/flushdns'], capture_output=True, timeout=30)
        if i18n.get_language() == 'ru':
            print("✓ Кэш DNS очищен")
        elif i18n.get_language() == 'en':
            print("✓ DNS cache flushed")
        elif i18n.get_language() == 'zh':
            print("✓ DNS缓存已清除")
        else:
            print("✓ DNS-Cache geleert")
        return True
    except Exception as e:
        if i18n.get_language() == 'ru':
            print(f"⚠ Ошибка очистки DNS: {e}")
        elif i18n.get_language() == 'en':
            print(f"⚠ DNS flush error: {e}")
        elif i18n.get_language() == 'zh':
            print(f"⚠ DNS清除错误：{e}")
        else:
            print(f"⚠ DNS-Löschfehler: {e}")
        return False

def _print_exe_blocked(exe_name):
    if i18n.get_language() == 'ru':
        print(f"✓ Запрещен запуск: {exe_name}")
    elif i18n.get_language() == 'en':
        print(f"✓ Blocked: {exe_name}")
    elif i18n.get_language() == 'zh':
        print(f"✓ 已禁止运行：{exe_name}")
    else:
        print(f"✓ Blockiert: {exe_name}")

def _merge_disallow_run(hive, explorer_path, disallow_path, executable_names):
    """Включает DisallowRun и добавляет exe в список (без перезаписи существующих)"""
    parent_path = explorer_path.rsplit('\\', 1)[0]
    for path in (parent_path, explorer_path, disallow_path):
        try:
            winreg.CreateKey(hive, path)
        except OSError:
            pass

    with winreg.OpenKey(hive, explorer_path, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, "DisallowRun", 0, winreg.REG_DWORD, 1)

    added_count = 0
    access = winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE | winreg.KEY_ENUMERATE_SUB_KEYS
    with winreg.OpenKey(hive, disallow_path, 0, access) as key:
        existing_entries = {}
        index = 0
        while True:
            try:
                name, value, _ = winreg.EnumValue(key, index)
                existing_entries[value.lower()] = name
                index += 1
            except OSError:
                break

        used_ids = set(existing_entries.values())
        counter = 1
        for exe_name in executable_names:
            exe_lower = exe_name.lower()
            if exe_lower in existing_entries:
                continue
            while str(counter) in used_ids:
                counter += 1
            reg_name = str(counter)
            winreg.SetValueEx(key, reg_name, 0, winreg.REG_SZ, exe_name)
            existing_entries[exe_lower] = reg_name
            used_ids.add(reg_name)
            _print_exe_blocked(exe_name)
            counter += 1
            added_count += 1
    return added_count

def block_program(program_name, executable_names, interactive=True):
    """Блокирует запуск программы через реестр"""
    print(t('block_program').format(program_name))
    
    if interactive:
        for i in range(3, 0, -1):
            if i18n.get_language() == 'ru':
                print(f"Ожидание: {i} секунд...", end='\r')
            elif i18n.get_language() == 'en':
                print(f"Waiting: {i} seconds...", end='\r')
            elif i18n.get_language() == 'zh':
                print(f"等待：{i}秒...", end='\r')
            else:
                print(f"Warten: {i} Sekunden...", end='\r')
            time.sleep(1)
        print(" " * 30, end='\r')
    
    try:
        policies_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies"
        explorer_path = policies_path + r"\Explorer"
        disallow_path = explorer_path + r"\DisallowRun"

        added_count = _merge_disallow_run(
            winreg.HKEY_LOCAL_MACHINE, explorer_path, disallow_path, executable_names
        )

        try:
            user_explorer_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"
            user_disallow_path = user_explorer_path + r"\DisallowRun"
            hkcu_added = _merge_disallow_run(
                winreg.HKEY_CURRENT_USER, user_explorer_path, user_disallow_path, executable_names
            )
            if i18n.get_language() == 'ru':
                print(f"✓ HKEY_CURRENT_USER: добавлено {hkcu_added} записей")
            elif i18n.get_language() == 'en':
                print(f"✓ HKEY_CURRENT_USER: {hkcu_added} entries added")
            elif i18n.get_language() == 'zh':
                print(f"✓ HKEY_CURRENT_USER：添加了 {hkcu_added} 条记录")
            else:
                print(f"✓ HKEY_CURRENT_USER: {hkcu_added} Einträge hinzugefügt")
        except Exception as e:
            if i18n.get_language() == 'ru':
                print(f"⚠ Предупреждение HKCU: {e}")
            elif i18n.get_language() == 'en':
                print(f"⚠ HKCU warning: {e}")
            elif i18n.get_language() == 'zh':
                print(f"⚠ HKCU警告：{e}")
            else:
                print(f"⚠ HKCU-Warnung: {e}")
        
        refresh_policy()
        
        if i18n.get_language() == 'ru':
            print(f"\n✓ {program_name} успешно заблокирована!")
            print(f"✓ Добавлено {added_count} новых ограничений")
        elif i18n.get_language() == 'en':
            print(f"\n✓ {program_name} successfully blocked!")
            print(f"✓ Added {added_count} new restrictions")
        elif i18n.get_language() == 'zh':
            print(f"\n✓ {program_name} 成功被拦截！")
            print(f"✓ 添加了 {added_count} 个新限制")
        else:
            print(f"\n✓ {program_name} erfolgreich blockiert!")
            print(f"✓ {added_count} neue Einschränkungen hinzugefügt")

        # Предлагаем перезагрузку только если были добавлены новые ограничения
        if added_count > 0:
            if interactive:
                return ask_reboot()
            return True
        else:
            if i18n.get_language() == 'ru':
                print("⚠ Новые ограничения не были добавлены (возможно, уже существуют)")
            elif i18n.get_language() == 'en':
                print("⚠ No new restrictions added (possibly already exist)")
            elif i18n.get_language() == 'zh':
                print("⚠ 未添加新限制（可能已存在）")
            else:
                print("⚠ Keine neuen Einschränkungen hinzugefügt (existieren möglicherweise bereits)")
            return False
        
    except Exception as e:
        if i18n.get_language() == 'ru':
            print(f"✗ Ошибка при блокировке: {e}")
        elif i18n.get_language() == 'en':
            print(f"✗ Blocking error: {e}")
        elif i18n.get_language() == 'zh':
            print(f"✗ 拦截时出错：{e}")
        else:
            print(f"✗ Blockierungsfehler: {e}")
        return False

def is_yandex_domain(host):
    if not host:
        return False
    if host in ("ya.ru", "dzen.ru") or host.endswith(".ya.ru"):
        return True
    markers = ("yandex", "yastatic", "yandexadexchange", "zen.yandex")
    return any(m in host for m in markers)

def _reg_set_dword(hive, path, name, value):
    try:
        winreg.CreateKey(hive, path)
        with winreg.OpenKey(hive, path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)
        return True
    except OSError:
        return False

def _reg_set_string(hive, path, name, value):
    try:
        winreg.CreateKey(hive, path)
        with winreg.OpenKey(hive, path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
        return True
    except OSError:
        return False

def _reg_delete_value(hive, path, name):
    try:
        with winreg.OpenKey(hive, path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, name)
        return True
    except OSError:
        return False

def _firewall_delete_group(group):
    for i in range(40):
        subprocess.run(
            ["netsh", "advfirewall", "firewall", "delete", "rule",
             f"name={FIREWALL_RULE_PREFIX}-{group}-{i}"],
            capture_output=True, text=True
        )

def _firewall_add_cidr_rules(group, cidrs, chunk_size=8):
    _firewall_delete_group(group)
    if not cidrs:
        return 0
    created = 0
    for idx in range(0, len(cidrs), chunk_size):
        chunk = cidrs[idx:idx + chunk_size]
        rule_name = f"{FIREWALL_RULE_PREFIX}-{group}-{idx // chunk_size}"
        result = subprocess.run(
            [
                "netsh", "advfirewall", "firewall", "add", "rule",
                f"name={rule_name}", "dir=out", "action=block", "enable=yes",
                f"remoteip={','.join(chunk)}",
            ],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            created += 1
        elif i18n.get_language() == 'ru':
            print(f"⚠ Firewall: {result.stderr.strip() or result.stdout.strip()}")
    return created

def harden_dns_bypass():
    """Усложняет обход блокировки через DoH / Secure DNS в браузерах и Windows"""
    if i18n.get_language() == 'ru':
        print("\n--- Защита от обхода DNS (DoH) ---")
    elif i18n.get_language() == 'en':
        print("\n--- DNS bypass protection (DoH) ---")
    else:
        print("\n--- DNS / DoH protection ---")

    ok = 0
    if _reg_set_string(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Google\Chrome", "DnsOverHttpsMode", "off"):
        ok += 1
    if _reg_set_string(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Edge", "DnsOverHttpsMode", "off"):
        ok += 1
    if _reg_set_dword(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Mozilla\Firefox\DNSOverHTTPS", "Enabled", 0):
        ok += 1

    _reg_set_dword(
        winreg.HKEY_LOCAL_MACHINE,
        r"SYSTEM\CurrentControlSet\Services\Dnscache\Parameters",
        "EnableAutoDoh", 0,
    )

    doh_hosts = _append_hosts_entries(DOH_BLOCK_DOMAINS, silent=True)
    if doh_hosts:
        if i18n.get_language() == 'ru':
            print(f"✓ В hosts добавлено {doh_hosts} записей DoH-серверов")
        elif i18n.get_language() == 'en':
            print(f"✓ Added {doh_hosts} DoH server entries to hosts")

    for proto, port in (("UDP", "853"), ("TCP", "853")):
        subprocess.run(
            [
                "netsh", "advfirewall", "firewall", "delete", "rule",
                f"name={FIREWALL_RULE_PREFIX}-DoH-{proto}",
            ],
            capture_output=True,
        )
        subprocess.run(
            [
                "netsh", "advfirewall", "firewall", "add", "rule",
                f"name={FIREWALL_RULE_PREFIX}-DoH-{proto}",
                "dir=out", "action=block", "enable=yes",
                f"protocol={proto}", f"remoteport={port}",
            ],
            capture_output=True, text=True,
        )

    if i18n.get_language() == 'ru':
        print(f"✓ Политики браузеров/Windows: {ok}, блокировка DNS-over-TLS (порт 853)")
        print("  VPN, Tor или мобильный интернет всё ещё могут обойти блокировку.")
    elif i18n.get_language() == 'en':
        print(f"✓ Browser/Windows policies: {ok}, DNS-over-TLS port 853 blocked")
        print("  VPN, Tor, or mobile data can still bypass blocking.")
    return True

def restore_dns_bypass_policies():
    policy_values = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Google\Chrome", "DnsOverHttpsMode"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Edge", "DnsOverHttpsMode"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Mozilla\Firefox\DNSOverHTTPS", "Enabled"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Dnscache\Parameters", "EnableAutoDoh"),
    ]
    for hive, path, name in policy_values:
        _reg_delete_value(hive, path, name)
    for proto in ("UDP", "TCP"):
        subprocess.run(
            ["netsh", "advfirewall", "firewall", "delete", "rule",
             f"name={FIREWALL_RULE_PREFIX}-DoH-{proto}"],
            capture_output=True,
        )

def remove_yandex_firewall_rules():
    _firewall_delete_group("Yandex4")
    _firewall_delete_group("Yandex6")

def block_yandex_network():
    """Блокирует исходящие подключения к подсетям Яндекса через брандмауэр Windows"""
    if i18n.get_language() == 'ru':
        print("\n--- Блокировка IP-сетей Яндекса (firewall) ---")
    elif i18n.get_language() == 'en':
        print("\n--- Blocking Yandex IP ranges (firewall) ---")
    n4 = _firewall_add_cidr_rules("Yandex4", YANDEX_IP_CIDRS_V4)
    n6 = _firewall_add_cidr_rules("Yandex6", YANDEX_IP_CIDRS_V6)
    if i18n.get_language() == 'ru':
        print(f"✓ Правила IPv4: {n4}, IPv6: {n6} (подсети AS13238)")
    elif i18n.get_language() == 'en':
        print(f"✓ IPv4 rules: {n4}, IPv6 rules: {n6} (AS13238)")
    return n4 + n6 > 0

def _append_hosts_entries(domains, silent=False):
    """Добавляет домены в hosts; возвращает число новых записей"""
    try:
        if not os.path.exists(HOSTS_BACKUP_PATH):
            shutil.copy2(HOSTS_PATH, HOSTS_BACKUP_PATH)
        content, file_encoding = read_hosts_file()
        entry_lines = []
        need_header = BLOCKER_HEADER not in content
        added_count = 0

        for site in domains:
            host = normalize_site(site)
            if not host:
                continue
            for entry in expand_site_entries(host):
                if site_blocked_in_hosts(content, entry):
                    continue
                entry_lines.append(f"127.0.0.1 {entry}\n")
                entry_lines.append(f"0.0.0.0 {entry}\n")
                content += f"127.0.0.1 {entry}\n"
                if not silent:
                    if i18n.get_language() == 'ru':
                        print(f"✓ Заблокирован: {entry}")
                    elif i18n.get_language() == 'en':
                        print(f"✓ Blocked: {entry}")
                added_count += 1

        if entry_lines:
            with open(HOSTS_PATH, 'a', encoding=file_encoding, errors='replace', newline='\n') as f:
                if need_header:
                    f.write(f"\n\n{BLOCKER_HEADER}\n")
                f.writelines(entry_lines)
        return added_count
    except OSError as e:
        if not silent:
            if i18n.get_language() == 'ru':
                print(f"✗ Ошибка hosts: {e}")
        return 0

def block_websites(websites, apply_yandex_firewall=False):
    """Блокирует сайты через hosts, усиление против DoH и (опционально) IP Яндекса"""
    print(t('block_websites'))
    
    try:
        hosts_list = []
        seen = set()
        for site in websites:
            host = normalize_site(site)
            if not host:
                if str(site).strip():
                    print_invalid_site(site)
                continue
            if host not in seen:
                seen.add(host)
                hosts_list.append(host)

        if any(is_yandex_domain(h) for h in hosts_list):
            apply_yandex_firewall = True

        added_count = _append_hosts_entries(hosts_list, silent=False)

        if added_count > 0:
            if i18n.get_language() == 'ru':
                print(f"\n✓ Заблокировано {added_count} записей в hosts")
            elif i18n.get_language() == 'en':
                print(f"\n✓ {added_count} entries added to hosts")
            elif i18n.get_language() == 'zh':
                print(f"\n✓ 已在hosts中添加 {added_count} 条记录")
            else:
                print(f"\n✓ {added_count} Einträge in hosts")
            flush_dns()
        elif hosts_list:
            if i18n.get_language() == 'ru':
                print("⚠ Домены уже были в hosts — применяем усиленную защиту...")
            elif i18n.get_language() == 'en':
                print("⚠ Domains already in hosts — applying extra protection...")

        harden_dns_bypass()
        if apply_yandex_firewall:
            block_yandex_network()

        if added_count > 0 or apply_yandex_firewall:
            if i18n.get_language() == 'ru':
                print(f"⚠ {t('browser_restart')}")
                print("  Полностью закройте браузер (все окна) и откройте снова.")
            elif i18n.get_language() == 'en':
                print(f"⚠ {t('browser_restart')}")
                print("  Fully quit the browser and open it again.")
            return True

        if i18n.get_language() == 'ru':
            print("⚠ Нечего блокировать — проверьте ввод домена")
        elif i18n.get_language() == 'en':
            print("⚠ Nothing to block — check domain input")
        return False
            
    except Exception as e:
        if i18n.get_language() == 'ru':
            print(f"✗ Ошибка при блокировке сайтов: {e}")
        elif i18n.get_language() == 'en':
            print(f"✗ Website blocking error: {e}")
        elif i18n.get_language() == 'zh':
            print(f"✗ 网站拦截时出错：{e}")
        else:
            print(f"✗ Website-Blockierungsfehler: {e}")
        return False

def unblock_all_programs():
    """Разблокирует все программы"""
    print(t('unblock_all_programs'))
    
    try:
        # Очищаем HKEY_LOCAL_MACHINE
        explorer_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer"
        disallow_path = explorer_path + r"\DisallowRun"
        
        # Отключаем политику
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, explorer_path, 0, winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, "DisallowRun", 0, winreg.REG_DWORD, 0)
        except:
            pass
        
        # Удаляем раздел с запрещенными программами
        try:
            winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, disallow_path)
            if i18n.get_language() == 'ru':
                print("✓ Раздел DisallowRun удален из HKEY_LOCAL_MACHINE")
            elif i18n.get_language() == 'en':
                print("✓ DisallowRun section removed from HKEY_LOCAL_MACHINE")
            elif i18n.get_language() == 'zh':
                print("✓ 已从HKEY_LOCAL_MACHINE删除DisallowRun部分")
            else:
                print("✓ DisallowRun-Bereich aus HKEY_LOCAL_MACHINE entfernt")
        except:
            pass
        
        # Очищаем HKEY_CURRENT_USER
        try:
            user_explorer_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"
            user_disallow_path = user_explorer_path + r"\DisallowRun"
            
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, user_explorer_path, 0, winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, "DisallowRun", 0, winreg.REG_DWORD, 0)
            
            try:
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, user_disallow_path)
                if i18n.get_language() == 'ru':
                    print("✓ Раздел DisallowRun удален из HKEY_CURRENT_USER")
                elif i18n.get_language() == 'en':
                    print("✓ DisallowRun section removed from HKEY_CURRENT_USER")
                elif i18n.get_language() == 'zh':
                    print("✓ 已从HKEY_CURRENT_USER删除DisallowRun部分")
                else:
                    print("✓ DisallowRun-Bereich aus HKEY_CURRENT_USER entfernt")
            except:
                pass
        except:
            pass
        
        # Применяем изменения
        refresh_policy()
        
        if i18n.get_language() == 'ru':
            print("✓ Все программы разблокированы!")
        elif i18n.get_language() == 'en':
            print("✓ All programs unblocked!")
        elif i18n.get_language() == 'zh':
            print("✓ 所有程序已解除拦截！")
        else:
            print("✓ Alle Programme freigeschaltet!")
        return True
        
    except Exception as e:
        if i18n.get_language() == 'ru':
            print(f"✗ Ошибка при разблокировке: {e}")
        elif i18n.get_language() == 'en':
            print(f"✗ Unblocking error: {e}")
        elif i18n.get_language() == 'zh':
            print(f"✗ 解除拦截时出错：{e}")
        else:
            print(f"✗ Freischaltfehler: {e}")
        return False

def unblock_all_websites():
    """Разблокирует все сайты"""
    print(t('unblock_all_websites'))
    
    try:
        if os.path.exists(HOSTS_BACKUP_PATH):
            shutil.copy2(HOSTS_BACKUP_PATH, HOSTS_PATH)
            if i18n.get_language() == 'ru':
                print("✓ Файл hosts восстановлен из резервной копии")
            elif i18n.get_language() == 'en':
                print("✓ Hosts file restored from backup")
            elif i18n.get_language() == 'zh':
                print("✓ hosts文件已从备份恢复")
            else:
                print("✓ Hosts-Datei aus Backup wiederhergestellt")
        else:
            content, encoding = read_hosts_file()
            new_lines = []
            skip_mode = False

            for line in content.splitlines(keepends=True):
                if BLOCKER_HEADER in line:
                    skip_mode = True
                    continue
                if skip_mode:
                    stripped = line.strip()
                    if not stripped:
                        skip_mode = False
                        continue
                    if stripped.startswith('#'):
                        continue
                    parts = stripped.split()
                    if len(parts) >= 2 and parts[0] in ('127.0.0.1', '0.0.0.0', '::1'):
                        continue
                new_lines.append(line)

            with open(HOSTS_PATH, 'w', encoding=encoding, newline='\n') as f:
                f.writelines(new_lines)
            
            if i18n.get_language() == 'ru':
                print("✓ Блокировки сайтов удалены из файла hosts")
            elif i18n.get_language() == 'en':
                print("✓ Website blocks removed from hosts file")
            elif i18n.get_language() == 'zh':
                print("✓ 已从hosts文件删除网站拦截")
            else:
                print("✓ Website-Blockierungen aus Hosts-Datei entfernt")
        
        flush_dns()
        restore_dns_bypass_policies()
        remove_yandex_firewall_rules()
        if i18n.get_language() == 'ru':
            print("✓ Правила firewall и политики DNS сняты")
        elif i18n.get_language() == 'en':
            print("✓ Firewall rules and DNS policies removed")
        if i18n.get_language() == 'ru':
            print("✓ Все сайты разблокированы!")
        elif i18n.get_language() == 'en':
            print("✓ All websites unblocked!")
        elif i18n.get_language() == 'zh':
            print("✓ 所有网站已解除拦截！")
        else:
            print("✓ Alle Websites freigeschaltet!")
        return True
        
    except Exception as e:
        if i18n.get_language() == 'ru':
            print(f"✗ Ошибка при разблокировке сайтов: {e}")
        elif i18n.get_language() == 'en':
            print(f"✗ Website unblocking error: {e}")
        elif i18n.get_language() == 'zh':
            print(f"✗ 解除网站拦截时出错：{e}")
        else:
            print(f"✗ Website-Freischaltfehler: {e}")
        return False

def view_current_blocks():
    """Просмотр текущих блокировок"""
    print(f"\n{t('current_blocks')}")
    print("="*50)
    
    total_blocks = 0
    
    # Проверяем HKEY_LOCAL_MACHINE
    try:
        disallow_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, disallow_path, 0, winreg.KEY_READ) as key:
            i = 0
            if i18n.get_language() == 'ru':
                print("HKEY_LOCAL_MACHINE:")
            elif i18n.get_language() == 'en':
                print("HKEY_LOCAL_MACHINE:")
            elif i18n.get_language() == 'zh':
                print("HKEY_LOCAL_MACHINE：")
            else:
                print("HKEY_LOCAL_MACHINE:")
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    print(f"  {name}: {value}")
                    i += 1
                except OSError:
                    break
            total_blocks += i
            if i == 0:
                print(f"  {t('no_programs')}")
    except OSError:
        if i18n.get_language() == 'ru':
            print("HKEY_LOCAL_MACHINE: Не настроено")
        elif i18n.get_language() == 'en':
            print("HKEY_LOCAL_MACHINE: Not configured")
        elif i18n.get_language() == 'zh':
            print("HKEY_LOCAL_MACHINE：未配置")
        else:
            print("HKEY_LOCAL_MACHINE: Nicht konfiguriert")
    
    # Проверяем HKEY_CURRENT_USER
    try:
        user_disallow_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, user_disallow_path, 0, winreg.KEY_READ) as key:
            i = 0
            if i18n.get_language() == 'ru':
                print("\nHKEY_CURRENT_USER:")
            elif i18n.get_language() == 'en':
                print("\nHKEY_CURRENT_USER:")
            elif i18n.get_language() == 'zh':
                print("\nHKEY_CURRENT_USER：")
            else:
                print("\nHKEY_CURRENT_USER:")
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    print(f"  {name}: {value}")
                    i += 1
                except OSError:
                    break
            total_blocks += i
            if i == 0:
                print(f"  {t('no_programs')}")
    except OSError:
        if i18n.get_language() == 'ru':
            print("HKEY_CURRENT_USER: Не настроено")
        elif i18n.get_language() == 'en':
            print("HKEY_CURRENT_USER: Not configured")
        elif i18n.get_language() == 'zh':
            print("HKEY_CURRENT_USER：未配置")
        else:
            print("HKEY_CURRENT_USER: Nicht konfiguriert")
    
    # Проверяем статус политики
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                           r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer", 
                           0, winreg.KEY_READ) as key:
            try:
                value, _ = winreg.QueryValueEx(key, "DisallowRun")
                status = t('enabled') if value == 1 else t('disabled')
                print(f"\n{t('policy_status')} {status}")
                print(f"{t('total_program_blocks')} {total_blocks}")
            except:
                print(f"\n{t('policy_status')} {t('not_configured')}")
    except:
        if i18n.get_language() == 'ru':
            print("\nНе удалось проверить статус политики")
        elif i18n.get_language() == 'en':
            print("\nFailed to check policy status")
        elif i18n.get_language() == 'zh':
            print("\n无法检查策略状态")
        else:
            print("\nKonnte Richtlinienstatus nicht überprüfen")
    
    # Показываем заблокированные сайты
    print("\n" + "="*50)
    print(t('blocked_sites'))
    try:
        content, _ = read_hosts_file()

        if BLOCKER_HEADER in content:
            lines = content.split('\n')
            site_count = 0
            in_blocked_section = False
            
            seen_sites = set()
            for line in lines:
                if BLOCKER_HEADER in line:
                    in_blocked_section = True
                    continue
                if in_blocked_section and line.strip() and not line.startswith('#'):
                    parts = line.split()
                    if len(parts) >= 2 and parts[0] in ('127.0.0.1', '0.0.0.0', '::1'):
                        site = parts[1].lower()
                        if site not in seen_sites:
                            seen_sites.add(site)
                            print(f"  {site}")
                            site_count += 1
            
            if site_count == 0:
                print(f"  {t('no_sites')}")
            else:
                print(f"{t('total_site_blocks')} {site_count}")
        else:
            print(f"  {t('no_sites')}")
    except Exception as e:
        if i18n.get_language() == 'ru':
            print(f"  Ошибка чтения файла hosts: {e}")
        elif i18n.get_language() == 'en':
            print(f"  Hosts file read error: {e}")
        elif i18n.get_language() == 'zh':
            print(f"  读取hosts文件时出错：{e}")
        else:
            print(f"  Hosts-Datei-Lesefehler: {e}")

def t_gui(key):
    """Перевод строк интерфейса GUI"""
    gui = LANGUAGES[i18n.get_language()].get('gui')
    if gui and key in gui:
        return gui[key]
    fallback = LANGUAGES['en'].get('gui', {})
    return fallback.get(key, key)

def get_programs_config():
    """Конфигурация блокируемых программ"""
    return {
        '1': {"name": t('programs')['1'], "executables": ["browser.exe", "yandex.exe", "YandexBrowser.exe"]},
        '2': {"name": t('programs')['2'], "executables": ["opera.exe", "opera_gx.exe"]},
        '3': {"name": t('programs')['3'], "executables": ["avastui.exe", "avast.exe", "avastsvchost.exe"]},
        '4': {"name": t('programs')['4'], "executables": ["360tray.exe", "360safe.exe", "360SD.exe"]},
        '5': {"name": t('programs')['5'], "executables": ["uTorrent.exe", "utorrent.exe"]},
        '6': {"name": t('programs')['6'], "executables": ["ccleaner.exe", "ccleaner64.exe"]},
        '7': {"name": t('programs')['7'], "executables": ["OneDrive.exe", "onedrive.exe", "OneDrive.Sync.Service.exe"]},
        '8': {"name": t('programs')['8'], "executables": ["max.exe", "Max.exe"]},
        '9': {"name": t('programs')['9'], "executables": ["mediaget.exe", "mgbot.exe"]},
        'ALL': {"name": t('programs')['ALL'], "executables": [
            "browser.exe", "yandex.exe", "YandexBrowser.exe", "opera.exe", "opera_gx.exe",
            "avastui.exe", "avast.exe", "avastsvchost.exe", "360tray.exe", "360safe.exe", "360SD.exe",
            "uTorrent.exe", "utorrent.exe", "ccleaner.exe", "ccleaner64.exe",
            "OneDrive.exe", "onedrive.exe", "OneDrive.Sync.Service.exe",
            "max.exe", "Max.exe", "mediaget.exe", "mgbot.exe",
        ]},
    }

def get_website_presets():
    """Предустановленные наборы сайтов"""
    return {
        '1': {"name": t('sites')['1'], "sites": YANDEX_BLOCK_DOMAINS, "yandex_firewall": True},
        '2': {"name": t('sites')['2'], "sites": ["mail.ru", "mail.com"]},
        '3': {"name": t('sites')['3'], "sites": ["utorrent.ru", "utorrent.com"]},
        '4': {"name": t('sites')['4'], "sites": ["max.ru", "max.com"]},
    }

def get_program_blocks():
    """Возвращает список (hive, id, exe) активных блокировок программ"""
    blocks = []
    for hive_label, hive, path in (
        ("HKLM", winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun"),
        ("HKCU", winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun"),
    ):
        try:
            with winreg.OpenKey(hive, path, 0, winreg.KEY_READ) as key:
                index = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, index)
                        blocks.append((hive_label, name, value))
                        index += 1
                    except OSError:
                        break
        except OSError:
            pass
    return blocks

def get_site_blocks():
    """Возвращает отсортированный список заблокированных доменов из hosts"""
    try:
        content, _ = read_hosts_file()
    except OSError:
        return []

    if BLOCKER_HEADER not in content:
        return []

    seen = set()
    sites = []
    in_section = False
    for line in content.splitlines():
        if BLOCKER_HEADER in line:
            in_section = True
            continue
        if not in_section:
            continue
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        parts = stripped.split()
        if len(parts) >= 2 and parts[0] in ('127.0.0.1', '0.0.0.0', '::1'):
            site = parts[1].lower()
            if site not in seen:
                seen.add(site)
                sites.append(site)
    return sorted(sites)

def get_disallow_run_status():
    """Статус политики DisallowRun"""
    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer",
            0, winreg.KEY_READ,
        ) as key:
            value, _ = winreg.QueryValueEx(key, "DisallowRun")
            return t('enabled') if value == 1 else t('disabled')
    except OSError:
        return t('not_configured')

def test_blocking():
    """Тестирование блокировки"""
    print(f"\n{t('testing_block')}")
    if i18n.get_language() == 'ru':
        print("Попробуйте запустить заблокированную программу.")
        print("Если блокировка работает, вы увидите сообщение об ошибке.")
        input("Нажмите Enter после тестирования...")
    elif i18n.get_language() == 'en':
        print("Try to run a blocked program.")
        print("If blocking works, you will see an error message.")
        input("Press Enter after testing...")
    elif i18n.get_language() == 'zh':
        print("尝试运行被拦截的程序。")
        print("如果拦截功能正常工作，您将看到错误消息。")
        input("测试后按Enter键...")
    else:
        print("Versuchen Sie, ein blockiertes Programm zu starten.")
        print("Wenn die Blockierung funktioniert, sehen Sie eine Fehlermeldung.")
        input("Drücken Sie Enter nach dem Testen...")

def print_watermark():
    watermark = f"""
    ╔══════════════════════════════════════════╗
    ║{t('title').center(38)}    ║
    ║{t('by').center(38)}    ║
    ║                                          ║
    ╚══════════════════════════════════════════╝
    """
    print(watermark)

def custom_block_websites():
    """Пользовательская блокировка сайтов"""
    print("\n" + "="*50)
    print(f" {t('site_blocking')}")
    print("="*50)
    print(t('enter_sites'))
    print(t('site_example'))
    print(t('finish_enter'))
    print("="*50)
    
    websites = []
    seen = set()
    while True:
        site_input = input(t('enter_site')).strip()
        if not site_input:
            break

        parts = re.split(r'[,;\s]+', site_input) if re.search(r'[,;\s]', site_input) else [site_input]
        for part in parts:
            part = part.strip()
            if not part:
                continue
            host = normalize_site(part)
            if not host:
                print_invalid_site(part)
                continue
            if host in seen:
                continue
            seen.add(host)
            websites.append(host)
    
    if websites:
        print(f"\n{t('will_block')} {', '.join(websites)}")
        confirm = input(t('continue_confirm'))
        if confirm_yes(confirm):
            if block_websites(websites):
                print(f"✓ {t('sites_blocked')}")
                print(f"⚠ {t('browser_restart')}")
            else:
                if i18n.get_language() == 'ru':
                    print("✗ Не удалось заблокировать сайты")
                elif i18n.get_language() == 'en':
                    print("✗ Failed to block websites")
                elif i18n.get_language() == 'zh':
                    print("✗ 无法拦截网站")
                else:
                    print("✗ Konnte Websites nicht blockieren")
    else:
        print(t('no_sites_entered'))

def change_language():
    """Смена языка интерфейса"""
    print("\n" + "="*50)
    print(f" {t('select_language')}")
    print("="*50)
    print("1. Русский (Russian)")
    print("2. English (English")
    print("3. 中国人 (Chinese)")
    print("4. Deutsch (German)")
    print("="*50)
    
    choice = input(t('choice'))
    if choice == '1':
        i18n.set_language('ru')
        print("✓ Язык изменен на русский")
    elif choice == '2':
        i18n.set_language('en')
        print("✓ Language changed to English")
    elif choice == '3':
        i18n.set_language('zh')
        print("✓ 语言已切换为中文")
    elif choice == '4':
        i18n.set_language('de')
        print("✓ Sprache auf Deutsch geändert")
    else:
        print(t('invalid_choice'))

def main():
    if not is_admin():
        run_as_admin()
        return
    
    while True:
        print_watermark()
        print(f" {t('admin_rights')}")
        print("="*55)
        print(f" {t('reboot_required')}")
        print("="*55)
        
        programs = get_programs_config()
        website_presets = get_website_presets()

        print("\n" + "="*50)
        print(f" {t('menu_title')}")
        print("="*50)
        for i, item in enumerate(t('menu_items'), 1):
            print(f"{i}. {item}")
        print("="*50)

        choice = input(f" {t('choice')}")

        if choice == '1':
            print(f"\n{t('select_program')}")
            for key, program in programs.items():
                print(f"{key}. {program['name']}")
            
            prog_choice = input(t('choice'))
            if prog_choice in programs:
                program_info = programs[prog_choice]
                if i18n.get_language() == 'ru':
                    print(f"\nБудут заблокированы: {', '.join(program_info['executables'])}")
                elif i18n.get_language() == 'en':
                    print(f"\nWill be blocked: {', '.join(program_info['executables'])}")
                elif i18n.get_language() == 'zh':
                    print(f"\n将拦截：{', '.join(program_info['executables'])}")
                else:
                    print(f"\nWird blockiert: {', '.join(program_info['executables'])}")
                confirm = input(t('continue_confirm')).lower()
                if confirm_yes(confirm):
                    need_reboot = block_program(program_info['name'], program_info['executables'])
                    if need_reboot:
                        reboot_computer()
            else:
                print(t('invalid_choice'))

        elif choice == '2':
            print(f"\n{t('site_options')}")
            for i, item in enumerate(t('site_choices'), 1):
                print(f"{i}. {item}")
            
            site_choice = input(t('choice'))
            
            if site_choice == '1':
                print(f"\n{t('select_site_category')}")
                for key, preset in website_presets.items():
                    preview = ', '.join(preset['sites'][:6])
                    if len(preset['sites']) > 6:
                        preview += f" (+{len(preset['sites']) - 6})"
                    print(f"{key}. {preset['name']} - {preview}")
                
                preset_choice = input(t('choice'))
                if preset_choice in website_presets:
                    preset_info = website_presets[preset_choice]
                    count = len(preset_info['sites'])
                    if preset_info.get('yandex_firewall'):
                        if i18n.get_language() == 'ru':
                            print(f"\n{t('will_block')} {count} доменов + IP-сети Яндекса + защита от DoH")
                        else:
                            print(f"\n{t('will_block')} {count} domains + Yandex IP ranges + DoH protection")
                    else:
                        print(f"\n{t('will_block')} {', '.join(preset_info['sites'])}")
                    confirm = input(t('continue_confirm'))
                    if confirm_yes(confirm):
                        if block_websites(
                            preset_info['sites'],
                            apply_yandex_firewall=preset_info.get('yandex_firewall', False),
                        ):
                            print(f"✓ {t('sites_blocked')}")
                else:
                    print(t('invalid_choice'))
                    
            elif site_choice == '2':
                custom_block_websites()

        elif choice == '3':
            confirm = input(f"{t('unblock_confirm')} ").lower()
            if confirm_yes(confirm):
                if unblock_all_programs():
                    if ask_reboot():
                        reboot_computer()

        elif choice == '4':
            confirm = input(f"{t('unblock_sites_confirm')} ").lower()
            if confirm_yes(confirm):
                unblock_all_websites()

        elif choice == '5':
            view_current_blocks()

        elif choice == '6':
            test_blocking()

        elif choice == '7':
            refresh_policy()
            flush_dns()

        elif choice == '8':
            change_language()

        elif choice == '9':
            print(t('exiting'))
            time.sleep(1)
            sys.exit()

        else:
            print(t('invalid_choice'))

        input(f"\n{t('enter_to_continue')}")


def launch_cli():
    """Консольный режим MurBlocker"""
    if not is_admin():
        run_as_admin(gui=False)
        return
    main()


def launch_gui(return_factory=False):
    """Графический режим MurBlocker. return_factory=True — вернуть класс UI для встраивания."""
    if not is_admin():
        if not return_factory:
            run_as_admin(gui=True)
        return None

    from gui_utils import hide_console, apply_window_icon
    if not return_factory:
        hide_console()

    try:
        import customtkinter as ctk
        from tkinter import messagebox
        import threading
    except ImportError:
        if not return_factory:
            print("customtkinter не установлен. Установите: pip install customtkinter")
            launch_cli()
        return None

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    ACCENT = "#6366f1"
    ACCENT_HOVER = "#4f46e5"
    CARD = "#1e293b"
    SIDEBAR = "#0f172a"
    LOG_BG = "#111827"

    class MurBlockerUI:
        """Интерфейс MurBlocker (отдельное окно или вкладка в MurTools)."""

        def __init__(self, container, root, embedded=False):
            self.root = root
            self.embedded = embedded
            self.container = container
            self._current_frame = "programs"
            container.grid_columnconfigure(0, weight=1)
            container.grid_rowconfigure(0, weight=1)
            self.shell = ctk.CTkFrame(container, fg_color="transparent", corner_radius=0)
            self.shell.grid(row=0, column=0, sticky="nsew")
            self.shell.grid_columnconfigure(0, weight=1)
            self._build_layout()
            self.show_frame("programs")
            self._log(t('admin_rights'))

        def _clear_shell(self):
            for widget in self.shell.winfo_children():
                widget.destroy()

        def rebuild(self):
            """Перестраивает UI после смены языка."""
            saved_log = ""
            if hasattr(self, "log_box"):
                try:
                    saved_log = self.log_box.get("1.0", "end")
                except Exception:
                    pass
            frame = self._current_frame
            self._build_layout()
            self.show_frame(frame)
            if saved_log.strip():
                self.log_box.configure(state="normal")
                self.log_box.insert("end", saved_log)
                self.log_box.configure(state="disabled")

        def _build_layout(self):
            self._clear_shell()
            if self.embedded:
                self.shell.grid_rowconfigure(1, weight=1)
                self._build_top_nav()
                content_row, content_col, log_row, log_col = 1, 0, 2, 0
                pad_x = (12, 12)
            else:
                self.shell.configure(fg_color="#0b1220")
                self.shell.grid_columnconfigure(0, weight=0, minsize=228)
                self.shell.grid_columnconfigure(1, weight=1)
                self.shell.grid_rowconfigure(0, weight=1)
                self.shell.grid_rowconfigure(1, weight=0)
                self._build_sidebar()
                content_row, content_col, log_row, log_col = 0, 1, 1, 1
                pad_x = (0, 16)

            self.content = ctk.CTkFrame(self.shell, fg_color="transparent")
            self.content.grid(
                row=content_row, column=content_col, sticky="nsew",
                padx=pad_x, pady=(12 if self.embedded else 16, 8),
            )
            self.content.grid_columnconfigure(0, weight=1)
            self.content.grid_rowconfigure(0, weight=1)
            self.frames = {
                "programs": self._create_programs_frame(),
                "sites": self._create_sites_frame(),
                "status": self._create_status_frame(),
                "tools": self._create_tools_frame(),
            }

            log_frame = ctk.CTkFrame(self.shell, fg_color=CARD, corner_radius=12)
            log_frame.grid(
                row=log_row, column=log_col, sticky="nsew",
                padx=pad_x, pady=(0, 12 if self.embedded else 20),
            )
            log_frame.grid_columnconfigure(0, weight=1)
            log_frame.grid_rowconfigure(1, weight=1)
            self._log_title = ctk.CTkLabel(
                log_frame, text=t_gui('log_title'), font=ctk.CTkFont(size=13, weight="bold"), anchor="w",
            )
            self._log_title.grid(row=0, column=0, padx=16, pady=(12, 4), sticky="w")
            self.log_box = ctk.CTkTextbox(
                log_frame, height=100 if self.embedded else 120,
                fg_color=LOG_BG, corner_radius=8,
                font=ctk.CTkFont(family="Consolas", size=12),
            )
            self.log_box.grid(row=1, column=0, padx=16, pady=(0, 12), sticky="nsew")
            self.log_box.configure(state="disabled")

        def _build_top_nav(self):
            bar = ctk.CTkFrame(self.shell, fg_color="transparent")
            bar.grid(row=0, column=0, sticky="ew", padx=12, pady=(8, 4))
            self.nav_buttons = {}
            for key, label_key in (
                ("programs", "nav_programs"),
                ("sites", "nav_sites"),
                ("status", "nav_status"),
                ("tools", "nav_tools"),
            ):
                btn = ctk.CTkButton(
                    bar, text=t_gui(label_key), height=36, corner_radius=8,
                    fg_color=CARD, hover_color=ACCENT, font=ctk.CTkFont(size=13),
                    command=lambda k=key: self.show_frame(k),
                )
                btn.pack(side="left", padx=4)
                self.nav_buttons[key] = btn

        def _build_sidebar(self):
            self.sidebar = ctk.CTkFrame(self.shell, width=228, corner_radius=0, fg_color=SIDEBAR)
            self.sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")
            self.sidebar.grid_propagate(False)

            inner = ctk.CTkFrame(self.sidebar, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=14, pady=14)
            inner.grid_columnconfigure(0, weight=1)

            icon_path = __import__("gui_utils").get_icon_path("murblocker")
            row = 0
            if icon_path and icon_path.lower().endswith(".png"):
                try:
                    self._logo_img = ctk.CTkImage(light_image=icon_path, dark_image=icon_path, size=(48, 48))
                    ctk.CTkLabel(inner, image=self._logo_img, text="").grid(row=row, column=0, pady=(0, 6))
                    row += 1
                except Exception:
                    pass

            ctk.CTkLabel(
                inner, text="MurBlocker", font=ctk.CTkFont(size=20, weight="bold"), text_color=ACCENT, anchor="w",
            ).grid(row=row, column=0, sticky="ew", pady=(0, 2))
            row += 1
            ctk.CTkLabel(
                inner, text=t_gui("subtitle"), font=ctk.CTkFont(size=11), text_color="#94a3b8", anchor="w",
            ).grid(row=row, column=0, sticky="ew", pady=(0, 2))
            row += 1
            ctk.CTkLabel(
                inner, text=t_gui("version_label"), font=ctk.CTkFont(size=10), text_color="#64748b", anchor="w",
            ).grid(row=row, column=0, sticky="ew", pady=(0, 14))
            row += 1

            self.nav_buttons = {}
            for key, label_key in (
                ("programs", "nav_programs"),
                ("sites", "nav_sites"),
                ("status", "nav_status"),
                ("tools", "nav_tools"),
            ):
                btn = ctk.CTkButton(
                    inner, text=t_gui(label_key), anchor="w", height=36, corner_radius=8,
                    fg_color="transparent", hover_color=CARD, font=ctk.CTkFont(size=13),
                    command=lambda k=key: self.show_frame(k),
                )
                btn.grid(row=row, column=0, sticky="ew", pady=2)
                self.nav_buttons[key] = btn
                row += 1

            inner.grid_rowconfigure(row, weight=1)
            row += 1

            admin_text = t_gui("admin_ok") if is_admin() else t_gui("no_admin")
            admin_color = "#22c55e" if is_admin() else "#ef4444"
            self._admin_lbl = ctk.CTkLabel(
                inner, text=f"● {admin_text}", font=ctk.CTkFont(size=11), text_color=admin_color, anchor="w",
            )
            self._admin_lbl.grid(row=row, column=0, sticky="ew", pady=(8, 4))
            row += 1

            self.lang_menu = ctk.CTkOptionMenu(
                inner, values=list(i18n.LANG_OPTIONS.values()),
                command=self._change_language, fg_color=CARD,
                button_color=ACCENT, button_hover_color=ACCENT_HOVER,
            )
            self.lang_menu.set(i18n.CODE_TO_LABEL[i18n.get_language()])
            self.lang_menu.grid(row=row, column=0, sticky="ew", pady=(0, 6))
            row += 1

            ctk.CTkButton(
                inner, text=t_gui("exit"), height=34, corner_radius=8,
                fg_color="#334155", hover_color="#475569", command=self.root.destroy,
            ).grid(row=row, column=0, sticky="ew")

        def _log(self, message):
            ts = datetime.now().strftime("%H:%M:%S")
            self.log_box.configure(state="normal")
            self.log_box.insert("end", f"[{ts}] {message}\n")
            self.log_box.see("end")
            self.log_box.configure(state="disabled")

        def _run_async(self, task, on_success=None):
            def worker():
                try:
                    result = task()
                    self.root.after(0, lambda: self._on_task_done(result, None, on_success))
                except Exception as exc:
                    self.root.after(0, lambda: self._on_task_done(None, exc, on_success))

            threading.Thread(target=worker, daemon=True).start()

        def _on_task_done(self, result, error, on_success):
            if error:
                self._log(f"{t_gui('error')}: {error}")
                messagebox.showerror(t_gui('error'), str(error))
            elif on_success:
                on_success(result)
            self.refresh_status_view()

        def show_frame(self, name):
            self._current_frame = name
            for key, btn in self.nav_buttons.items():
                if self.embedded:
                    btn.configure(fg_color=ACCENT if key == name else CARD)
                else:
                    btn.configure(fg_color=ACCENT if key == name else "transparent")
            for frame in self.frames.values():
                frame.grid_forget()
            self.frames[name].grid(row=0, column=0, sticky="nsew")
            if name == "status":
                self.refresh_status_view()

        def _create_programs_frame(self):
            frame = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
            frame.grid_columnconfigure(0, weight=1)

            header = ctk.CTkFrame(frame, fg_color="transparent")
            header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
            header.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                header, text=t_gui('nav_programs'), font=ctk.CTkFont(size=22, weight="bold"), anchor="w",
            ).grid(row=0, column=0, sticky="w")

            programs = get_programs_config()
            row = 1
            for key in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                info = programs[key]
                card = ctk.CTkFrame(frame, fg_color=CARD, corner_radius=10)
                card.grid(row=row, column=0, sticky="ew", pady=5)
                card.grid_columnconfigure(0, weight=1)

                text_col = ctk.CTkFrame(card, fg_color="transparent")
                text_col.grid(row=0, column=0, sticky="ew", padx=16, pady=12)
                text_col.grid_columnconfigure(0, weight=1)
                ctk.CTkLabel(
                    text_col, text=info['name'], font=ctk.CTkFont(size=14, weight="bold"), anchor="w",
                ).grid(row=0, column=0, sticky="w")
                exe_text = ", ".join(info['executables'][:3])
                if len(info['executables']) > 3:
                    exe_text += "..."
                ctk.CTkLabel(
                    text_col, text=exe_text, text_color="#94a3b8",
                    font=ctk.CTkFont(size=11), anchor="w", wraplength=520,
                ).grid(row=1, column=0, sticky="w", pady=(4, 0))

                ctk.CTkButton(
                    card, text=t_gui('block_btn'), width=120, height=34,
                    fg_color=ACCENT, hover_color=ACCENT_HOVER, corner_radius=8,
                    command=lambda i=info: self._block_program(i),
                ).grid(row=0, column=1, padx=16, pady=12)
                row += 1

            all_info = programs['ALL']
            all_card = ctk.CTkFrame(frame, fg_color="#312e81", corner_radius=12)
            all_card.grid(row=row, column=0, sticky="ew", pady=(12, 0))
            all_card.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                all_card, text=all_info['name'], font=ctk.CTkFont(size=16, weight="bold"),
            ).grid(row=0, column=0, padx=16, pady=16, sticky="w")
            ctk.CTkButton(
                all_card, text=t_gui('block_all_btn'), width=160, height=36,
                fg_color="#ef4444", hover_color="#dc2626", corner_radius=8,
                command=lambda: self._block_program(all_info),
            ).grid(row=0, column=1, padx=16, pady=16)
            return frame

        def _create_sites_frame(self):
            frame = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
            frame.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                frame, text=t_gui('nav_sites'), font=ctk.CTkFont(size=22, weight="bold"), anchor="w",
            ).grid(row=0, column=0, sticky="w", pady=(0, 8))
            ctk.CTkLabel(
                frame, text=t('reboot_required'), text_color="#fbbf24",
                font=ctk.CTkFont(size=12), wraplength=700, justify="left",
            ).grid(row=1, column=0, sticky="w", pady=(0, 16))

            ctk.CTkLabel(
                frame, text=t_gui('presets_title'), font=ctk.CTkFont(size=14, weight="bold"), anchor="w",
            ).grid(row=2, column=0, sticky="w", pady=(0, 8))

            presets = get_website_presets()
            preset_row = ctk.CTkFrame(frame, fg_color="transparent")
            preset_row.grid(row=3, column=0, sticky="ew", pady=(0, 20))
            for idx, preset in presets.items():
                count = len(preset['sites'])
                label = f"{preset['name']} ({count})"
                ctk.CTkButton(
                    preset_row, text=label, height=38, corner_radius=10,
                    fg_color=CARD, hover_color=ACCENT,
                    command=lambda p=preset: self._block_sites_preset(p),
                ).grid(row=0, column=int(idx) - 1, padx=6, pady=4)

            manual = ctk.CTkFrame(frame, fg_color=CARD, corner_radius=12)
            manual.grid(row=4, column=0, sticky="ew", pady=8)
            manual.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                manual, text=t_gui('custom_site_label'), anchor="w",
                font=ctk.CTkFont(size=13),
            ).grid(row=0, column=0, columnspan=2, padx=16, pady=(14, 4), sticky="w")
            ctk.CTkLabel(
                manual, text=t_gui('manual_sites_hint'), text_color="#94a3b8",
                font=ctk.CTkFont(size=11), anchor="w",
            ).grid(row=1, column=0, columnspan=2, padx=16, pady=(0, 8), sticky="w")

            self.site_entry = ctk.CTkEntry(
                manual, placeholder_text="vk.com, youtube.com", height=38, corner_radius=8,
            )
            self.site_entry.grid(row=2, column=0, padx=16, pady=(0, 14), sticky="ew")
            ctk.CTkButton(
                manual, text=t_gui('custom_site_block'), width=180, height=38,
                fg_color=ACCENT, hover_color=ACCENT_HOVER, corner_radius=8,
                command=self._block_custom_sites,
            ).grid(row=2, column=1, padx=16, pady=(0, 14))
            return frame

        def _create_status_frame(self):
            frame = ctk.CTkFrame(self.content, fg_color="transparent")
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(2, weight=1)

            header = ctk.CTkFrame(frame, fg_color="transparent")
            header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
            header.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                header, text=t_gui('nav_status'), font=ctk.CTkFont(size=22, weight="bold"), anchor="w",
            ).grid(row=0, column=0, sticky="w")
            ctk.CTkButton(
                header, text="↻", width=40, height=32, corner_radius=8,
                fg_color=CARD, hover_color=ACCENT, command=self.refresh_status_view,
            ).grid(row=0, column=1)

            self.policy_label = ctk.CTkLabel(
                frame, text="", font=ctk.CTkFont(size=13), anchor="w", text_color="#94a3b8",
            )
            self.policy_label.grid(row=1, column=0, sticky="w", pady=(0, 12))

            columns = ctk.CTkFrame(frame, fg_color="transparent")
            columns.grid(row=2, column=0, sticky="nsew")
            columns.grid_columnconfigure((0, 1), weight=1)
            columns.grid_rowconfigure(0, weight=1)

            prog_box = ctk.CTkFrame(columns, fg_color=CARD, corner_radius=12)
            prog_box.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
            prog_box.grid_rowconfigure(1, weight=1)
            prog_box.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                prog_box, text=t_gui('blocked_programs'), font=ctk.CTkFont(size=14, weight="bold"),
            ).grid(row=0, column=0, padx=16, pady=12, sticky="w")
            self.prog_list = ctk.CTkTextbox(prog_box, fg_color=LOG_BG, corner_radius=8)
            self.prog_list.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="nsew")

            site_box = ctk.CTkFrame(columns, fg_color=CARD, corner_radius=12)
            site_box.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
            site_box.grid_rowconfigure(1, weight=1)
            site_box.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                site_box, text=t_gui('blocked_sites'), font=ctk.CTkFont(size=14, weight="bold"),
            ).grid(row=0, column=0, padx=16, pady=12, sticky="w")
            self.site_list = ctk.CTkTextbox(site_box, fg_color=LOG_BG, corner_radius=8)
            self.site_list.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="nsew")
            return frame

        def _create_tools_frame(self):
            frame = ctk.CTkFrame(self.content, fg_color="transparent")
            frame.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                frame, text=t_gui('nav_tools'), font=ctk.CTkFont(size=22, weight="bold"), anchor="w",
            ).grid(row=0, column=0, sticky="w", pady=(0, 20))

            tools = (
                (t_gui('unblock_programs'), self._unblock_programs, "#ef4444"),
                (t_gui('unblock_sites'), self._unblock_sites, "#f97316"),
                (t_gui('refresh_policies_btn'), self._refresh_policies, ACCENT),
                (t_gui('flush_dns_btn'), self._flush_dns, "#0ea5e9"),
            )
            for idx, (label, cmd, color) in enumerate(tools, start=1):
                ctk.CTkButton(
                    frame, text=label, height=48, corner_radius=12,
                    fg_color=color, hover_color=ACCENT_HOVER, anchor="w",
                    font=ctk.CTkFont(size=14), command=cmd,
                ).grid(row=idx, column=0, sticky="ew", pady=8)
            return frame

        def refresh_status_view(self):
            if not hasattr(self, 'prog_list'):
                return
            blocks = get_program_blocks()
            sites = get_site_blocks()
            self.policy_label.configure(text=f"{t_gui('policy_label')} {get_disallow_run_status()}")

            self.prog_list.configure(state="normal")
            self.prog_list.delete("1.0", "end")
            if blocks:
                for hive, reg_id, exe in blocks:
                    self.prog_list.insert("end", f"[{hive}] {exe}\n")
            else:
                self.prog_list.insert("end", t('no_programs') + "\n")
            self.prog_list.configure(state="disabled")

            self.site_list.configure(state="normal")
            self.site_list.delete("1.0", "end")
            if sites:
                for site in sites:
                    self.site_list.insert("end", f"• {site}\n")
            else:
                self.site_list.insert("end", t('no_sites') + "\n")
            self.site_list.configure(state="disabled")

        def _change_language(self, choice):
            i18n.set_language_from_label(choice)
            self.rebuild()
            messagebox.showinfo(t_gui('done'), t_gui('lang_changed'))

        def _block_program(self, info):
            if not messagebox.askyesno(t_gui('confirm'), t_gui('confirm_block_prog').format(info['name'])):
                return
            self._log(t('block_program').format(info['name']))

            def task():
                return block_program(info['name'], info['executables'], interactive=False)

            def done(need_reboot):
                self._log(t_gui('done'))
                if need_reboot and messagebox.askyesno(t_gui('confirm'), t_gui('confirm_reboot')):
                    reboot_computer()

            self._run_async(task, on_success=done)

        def _block_sites_preset(self, preset):
            self._log(t('block_websites') + f" — {preset['name']}")

            def task():
                return block_websites(
                    preset['sites'],
                    apply_yandex_firewall=preset.get('yandex_firewall', False),
                )

            def done(ok):
                if ok:
                    self._log(t('sites_blocked'))
                    messagebox.showinfo(t_gui('done'), t('sites_blocked') + "\n" + t('browser_restart'))

            self._run_async(task, on_success=done)

        def _block_custom_sites(self):
            raw = self.site_entry.get().strip()
            if not raw:
                messagebox.showwarning(t_gui('error'), t('no_sites_entered'))
                return
            sites = []
            seen = set()
            for part in re.split(r'[,;\s]+', raw):
                host = normalize_site(part.strip())
                if not host:
                    continue
                if host not in seen:
                    seen.add(host)
                    sites.append(host)
            if not sites:
                messagebox.showwarning(t_gui('error'), t('no_sites_entered'))
                return
            self._log(f"{t('will_block')} {', '.join(sites)}")

            def task():
                return block_websites(sites)

            def done(ok):
                if ok:
                    self.site_entry.delete(0, "end")
                    self._log(t('sites_blocked'))

            self._run_async(task, on_success=done)

        def _unblock_programs(self):
            if not messagebox.askyesno(t_gui('confirm'), t_gui('confirm_unblock_prog')):
                return
            self._log(t('unblock_all_programs'))

            def task():
                return unblock_all_programs()

            def done(ok):
                if ok and messagebox.askyesno(t_gui('confirm'), t_gui('confirm_reboot')):
                    reboot_computer()

            self._run_async(task, on_success=done)

        def _unblock_sites(self):
            if not messagebox.askyesno(t_gui('confirm'), t_gui('confirm_unblock_sites')):
                return
            self._log(t('unblock_all_websites'))
            self._run_async(unblock_all_websites, on_success=lambda _: self._log(t_gui('done')))

        def _refresh_policies(self):
            self._log(t('refresh_policies'))
            self._run_async(refresh_policy, on_success=lambda _: self._log(t_gui('done')))

        def _flush_dns(self):
            self._log("DNS...")
            self._run_async(flush_dns, on_success=lambda _: self._log(t_gui('done')))

    if return_factory:
        return MurBlockerUI

    root = ctk.CTk()
    root.title(t_gui('window_title'))
    root.geometry("980x680")
    root.minsize(860, 600)
    root.configure(fg_color="#0b1220")
    apply_window_icon(root, "murblocker")
    holder = ctk.CTkFrame(root, fg_color="transparent")
    holder.pack(fill="both", expand=True)
    MurBlockerUI(holder, root, embedded=False)
    root.mainloop()


def embed_murblocker(parent_frame, root_window):
    """Встраивает MurBlocker во вкладку MurTools."""
    ui_cls = launch_gui(return_factory=True)
    if ui_cls is None:
        return None
    return ui_cls(parent_frame, root_window, embedded=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("--cli", "-c", "cli"):
        launch_cli()
    else:
        launch_gui()