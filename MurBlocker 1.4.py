import sys
import os
import time
import ctypes
import winreg
import subprocess
import shutil
from datetime import datetime
from colorama import init, Fore, Back, Style

# Языковые настройки
LANGUAGES = {
    'ru': {   
        'title': "БЛОКИРОВЩИК ПРОГРАММ 1.4",
        'by': "by BarsikYT",
        'admin_rights': "Программа запущена с правами администратора",
        'reboot_required': "ВАЖНО: Для работы блокировок требуется перезагрузка!",
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
        'site_example': "Пример: yandex.ru, dzen.ru, vk.com",
        'finish_enter': "Для завершения ввода введите пустую строку",
        'enter_site': "Введите сайт (или Enter для завершения):",
        'will_block': "Будут заблокированы:",
        'sites_blocked': "Сайты успешно заблокированы!",
        'browser_restart': "Для применения изменений может потребоваться перезагрузка браузера",
        'no_sites_entered': "Не введено ни одного сайта",
        'site_options': "Блокировка сайтов:",
        'site_choices': [
            "Выбрать из списка",
            "Ввести вручную"
        ],
        'blocked_sites': "Заблокированные сайты:",
        'select_language': "Выберите язык / Select language:",
        'language_changed': "Язык изменен на русский"
    },
    'en': {
        'title': "PROGRAM BLOCKER 1.4", 
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
        'language_changed': "Language changed to English"
    },
    'zh': {
        'title': "程序拦截器 1.4",
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
        'title': "PROGRAMM-BLOCKER 1.4",
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

# Текущий язык (по умолчанию русский)
current_language = 'ru'

def t(key):
    """Функция для перевода текста"""
    return LANGUAGES[current_language].get(key, key)

def is_admin():
    """Проверяет, запущена ли программа от имени администратора"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Перезапускает программу с правами администратора"""
    if is_admin():
        return True
    
    if current_language == 'ru':
        print("Программа требует права администратора...")
    elif current_language == 'en':
        print("Program requires administrator rights...")
    elif current_language == 'zh':
        print("程序需要管理员权限...")
    else:
        print("Programm erfordert Administratorrechte...")
    
    time.sleep(2)
    
    script = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
    
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script}"', None, 1
        )
    except Exception as e:
        if current_language == 'ru':
            print(f"Ошибка при запросе прав администратора: {e}")
            input("Нажмите Enter для выхода...")
        elif current_language == 'en':
            print(f"Error requesting admin rights: {e}")
            input("Press Enter to exit...")
        elif current_language == 'zh':
            print(f"请求管理员权限时出错：{e}")
            input("按Enter键退出...")
        else:
            print(f"Fehler beim Anfordern von Administratorrechten: {e}")
            input("Drücken Sie Enter zum Beenden...")
    
    sys.exit(0)

def reboot_computer():
    """Выполняет перезагрузку компьютера"""
    print("\n" + "="*50)
    if current_language == 'ru':
        print(" ПЕРЕЗАГРУЗКА КОМПЬЮТЕРА")
        print("Компьютер будет перезагружен через 10 секунд...")
        print("Сохраните все важные данные!")
    elif current_language == 'en':
        print(" COMPUTER REBOOT")
        print("Computer will reboot in 10 seconds...")
        print("Save all important data!")
    elif current_language == 'zh':
        print(" 计算机重启")
        print("计算机将在10秒后重启...")
        print("请保存所有重要数据！")
    else:
        print(" COMPUTER-NEUSTART")
        print("Computer wird in 10 Sekunden neu gestartet...")
        print("Speichern Sie alle wichtigen Daten!")
    print("="*50)
    
    for i in range(10, 0, -1):
        if current_language == 'ru':
            print(f"Перезагрузка через: {i} секунд...", end='\r')
        elif current_language == 'en':
            print(f"Reboot in: {i} seconds...", end='\r')
        elif current_language == 'zh':
            print(f"重启倒计时：{i}秒...", end='\r')
        else:
            print(f"Neustart in: {i} Sekunden...", end='\r')
        time.sleep(1)
    
    if current_language == 'ru':
        print("Выполняется перезагрузка...")
    elif current_language == 'en':
        print("Rebooting...")
    elif current_language == 'zh':
        print("正在重启...")
    else:
        print("Starte neu...")
    try:
        os.system("shutdown /r /t 0")
    except Exception as e:
        if current_language == 'ru':
            print(f"Ошибка при перезагрузке: {e}")
        elif current_language == 'en':
            print(f"Reboot error: {e}")
        elif current_language == 'zh':
            print(f"重启时出错：{e}")
        else:
            print(f"Fehler beim Neustart: {e}")

def ask_reboot():
    """Спрашивает пользователя о перезагрузке"""
    print("\n" + "="*50)
    if current_language == 'ru':
        print(" ДЛЯ ПРИМЕНЕНИЯ ИЗМЕНЕНИЙ ТРЕБУЕТСЯ ПЕРЕЗАГРУЗКА")
        print("Блокировка будет работать только после перезагрузки!")
        print("Выберите действие:")
        print("1. Перезагрузить сейчас (y)")
        print("2. Перезагрузить позже (n)")
    elif current_language == 'en':
        print(" REBOOT REQUIRED FOR CHANGES TO TAKE EFFECT")
        print("Blocking will only work after reboot!")
        print("Choose action:")
        print("1. Reboot now (y)")
        print("2. Reboot later (n)")
    elif current_language == 'zh':
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
            if current_language == 'ru':
                print("Пожалуйста, введите 'y' (да) или 'n' (нет)")
            elif current_language == 'en':
                print("Please enter 'y' (yes) or 'n' (no)")
            elif current_language == 'zh':
                print("请输入 'y' (是) 或 'n' (否)")
            else:
                print("Bitte geben Sie 'j' (ja) oder 'n' (nein) ein")

def refresh_policy():
    """Обновляет групповые политики для применения изменений"""
    try:
        print(t('refresh_policies'))
        result = subprocess.run(['gpupdate', '/force'], capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            if current_language == 'ru':
                print("✓ Политики обновлены")
            elif current_language == 'en':
                print("✓ Policies updated")
            elif current_language == 'zh':
                print("✓ 策略已更新")
            else:
                print("✓ Richtlinien aktualisiert")
        else:
            if current_language == 'ru':
                print("⚠ gpupdate завершился с ошибкой, пробуем альтернативный метод...")
            elif current_language == 'en':
                print("⚠ gpupdate failed, trying alternative method...")
            elif current_language == 'zh':
                print("⚠ gpupdate失败，尝试替代方法...")
            else:
                print("⚠ gpupdate fehlgeschlagen, versuche alternative Methode...")
            subprocess.run(['taskkill', '/f', '/im', 'explorer.exe'], capture_output=True)
            time.sleep(2)
            subprocess.Popen('explorer.exe')
            if current_language == 'ru':
                print("✓ Проводник перезапущен")
            elif current_language == 'en':
                print("✓ Explorer restarted")
            elif current_language == 'zh':
                print("✓ 资源管理器已重启")
            else:
                print("✓ Explorer neu gestartet")
        return True
    except Exception as e:
        if current_language == 'ru':
            print(f"⚠ Ошибка обновления политик: {e}")
        elif current_language == 'en':
            print(f"⚠ Policy update error: {e}")
        elif current_language == 'zh':
            print(f"⚠ 策略更新错误：{e}")
        else:
            print(f"⚠ Richtlinienaktualisierungsfehler: {e}")
        return False

def flush_dns():
    """Очищает кэш DNS"""
    try:
        if current_language == 'ru':
            print("Очистка кэша DNS...")
        elif current_language == 'en':
            print("Flushing DNS cache...")
        elif current_language == 'zh':
            print("正在清除DNS缓存...")
        else:
            print("Leere DNS-Cache...")
        subprocess.run(['ipconfig', '/flushdns'], capture_output=True, timeout=30)
        if current_language == 'ru':
            print("✓ Кэш DNS очищен")
        elif current_language == 'en':
            print("✓ DNS cache flushed")
        elif current_language == 'zh':
            print("✓ DNS缓存已清除")
        else:
            print("✓ DNS-Cache geleert")
        return True
    except Exception as e:
        if current_language == 'ru':
            print(f"⚠ Ошибка очистки DNS: {e}")
        elif current_language == 'en':
            print(f"⚠ DNS flush error: {e}")
        elif current_language == 'zh':
            print(f"⚠ DNS清除错误：{e}")
        else:
            print(f"⚠ DNS-Löschfehler: {e}")
        return False

def block_program(program_name, executable_names):
    """Блокирует запуск программы через реестр"""
    print(t('block_program').format(program_name))
    
    for i in range(3, 0, -1):
        if current_language == 'ru':
            print(f"Ожидание: {i} секунд...", end='\r')
        elif current_language == 'en':
            print(f"Waiting: {i} seconds...", end='\r')
        elif current_language == 'zh':
            print(f"等待：{i}秒...", end='\r')
        else:
            print(f"Warten: {i} Sekunden...", end='\r')
        time.sleep(1)
    print(" " * 30, end='\r')
    
    try:
        # Основной путь для политик
        policies_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies"
        explorer_path = policies_path + r"\Explorer"
        disallow_path = explorer_path + r"\DisallowRun"
        
        # Создаем необходимые разделы
        try:
            winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, policies_path)
        except:
            pass
            
        try:
            winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, explorer_path)
        except:
            pass
        
        # ВКЛЮЧАЕМ политику DisallowRun
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, explorer_path, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "DisallowRun", 0, winreg.REG_DWORD, 1)
        
        # Создаем раздел DisallowRun
        try:
            winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, disallow_path)
        except:
            pass
        
        # Добавляем исполняемые файлы
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, disallow_path, 0, winreg.KEY_WRITE) as key:
            # Получаем текущие записи
            existing_entries = {}
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    existing_entries[value.lower()] = name
                    i += 1
                except WindowsError:
                    break
            
            # Добавляем новые записи
            counter = 1
            added_count = 0
            for exe_name in executable_names:
                if exe_name.lower() not in existing_entries:
                    # Ищем свободный номер
                    while str(counter) in [existing_entries.get(k) for k in existing_entries]:
                        counter += 1
                    
                    winreg.SetValueEx(key, str(counter), 0, winreg.REG_SZ, exe_name)
                    if current_language == 'ru':
                        print(f"✓ Запрещен запуск: {exe_name}")
                    elif current_language == 'en':
                        print(f"✓ Blocked: {exe_name}")
                    elif current_language == 'zh':
                        print(f"✓ 已禁止运行：{exe_name}")
                    else:
                        print(f"✓ Blockiert: {exe_name}")
                    counter += 1
                    added_count += 1
        
        # Дублируем в HKEY_CURRENT_USER для надежности
        try:
            user_explorer_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"
            user_disallow_path = user_explorer_path + r"\DisallowRun"
            
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, user_explorer_path, 0, winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, "DisallowRun", 0, winreg.REG_DWORD, 1)
            
            try:
                winreg.CreateKey(winreg.HKEY_CURRENT_USER, user_disallow_path)
            except:
                pass
            
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, user_disallow_path, 0, winreg.KEY_WRITE) as key:
                counter = 1
                for exe_name in executable_names:
                    winreg.SetValueEx(key, str(counter), 0, winreg.REG_SZ, exe_name)
                    counter += 1
            
            if current_language == 'ru':
                print("✓ Настройки продублированы в HKEY_CURRENT_USER")
            elif current_language == 'en':
                print("✓ Settings duplicated in HKEY_CURRENT_USER")
            elif current_language == 'zh':
                print("✓ 设置已复制到HKEY_CURRENT_USER")
            else:
                print("✓ Einstellungen in HKEY_CURRENT_USER dupliziert")
        except Exception as e:
            if current_language == 'ru':
                print(f"⚠ Предупреждение HKCU: {e}")
            elif current_language == 'en':
                print(f"⚠ HKCU warning: {e}")
            elif current_language == 'zh':
                print(f"⚠ HKCU警告：{e}")
            else:
                print(f"⚠ HKCU-Warnung: {e}")
        
        # Применяем изменения
        refresh_policy()
        
        if current_language == 'ru':
            print(f"\n✓ {program_name} успешно заблокирована!")
            print(f"✓ Добавлено {added_count} новых ограничений")
        elif current_language == 'en':
            print(f"\n✓ {program_name} successfully blocked!")
            print(f"✓ Added {added_count} new restrictions")
        elif current_language == 'zh':
            print(f"\n✓ {program_name} 成功被拦截！")
            print(f"✓ 添加了 {added_count} 个新限制")
        else:
            print(f"\n✓ {program_name} erfolgreich blockiert!")
            print(f"✓ {added_count} neue Einschränkungen hinzugefügt")

        # Предлагаем перезагрузку только если были добавлены новые ограничения
        if added_count > 0:
            return ask_reboot()
        else:
            if current_language == 'ru':
                print("⚠ Новые ограничения не были добавлены (возможно, уже существуют)")
            elif current_language == 'en':
                print("⚠ No new restrictions added (possibly already exist)")
            elif current_language == 'zh':
                print("⚠ 未添加新限制（可能已存在）")
            else:
                print("⚠ Keine neuen Einschränkungen hinzugefügt (existieren möglicherweise bereits)")
            return False
        
    except Exception as e:
        if current_language == 'ru':
            print(f"✗ Ошибка при блокировке: {e}")
        elif current_language == 'en':
            print(f"✗ Blocking error: {e}")
        elif current_language == 'zh':
            print(f"✗ 拦截时出错：{e}")
        else:
            print(f"✗ Blockierungsfehler: {e}")
        return False

def block_websites(websites):
    """Блокирует сайты через файл hosts"""
    print(t('block_websites'))
    
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    backup_path = r"C:\Windows\System32\drivers\etc\hosts.backup"
    
    try:
        # Создаем резервную копию
        if not os.path.exists(backup_path):
            shutil.copy2(hosts_path, backup_path)
            if current_language == 'ru':
                print("✓ Создана резервная копия hosts файла")
            elif current_language == 'en':
                print("✓ Hosts file backup created")
            elif current_language == 'zh':
                print("✓ 已创建hosts文件备份")
            else:
                print("✓ Hosts-Datei-Backup erstellt")
        
        # Читаем текущий файл hosts
        with open(hosts_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем, есть ли уже наши блокировки
        blocker_header = "# === BLOCKED BY BARSIKYT BLOCKER ==="
        if blocker_header not in content:
            content += f"\n\n{blocker_header}\n"
        
        # Добавляем блокировки
        added_count = 0
        with open(hosts_path, 'a', encoding='utf-8') as f:
            for site in websites:
                site = site.strip()
                if not site:
                    continue
                
                # Проверяем, не заблокирован ли уже сайт
                if f"127.0.0.1 {site}" not in content and f"0.0.0.0 {site}" not in content:
                    f.write(f"127.0.0.1 {site}\n")
                    f.write(f"0.0.0.0 {site}\n")
                    if current_language == 'ru':
                        print(f"✓ Заблокирован: {site}")
                    elif current_language == 'en':
                        print(f"✓ Blocked: {site}")
                    elif current_language == 'zh':
                        print(f"✓ 已拦截：{site}")
                    else:
                        print(f"✓ Blockiert: {site}")
                    added_count += 1
                else:
                    if current_language == 'ru':
                        print(f"⚠ Уже заблокирован: {site}")
                    elif current_language == 'en':
                        print(f"⚠ Already blocked: {site}")
                    elif current_language == 'zh':
                        print(f"⚠ 已拦截：{site}")
                    else:
                        print(f"⚠ Bereits blockiert: {site}")
        
        if added_count > 0:
            if current_language == 'ru':
                print(f"\n✓ Заблокировано {added_count} сайтов")
            elif current_language == 'en':
                print(f"\n✓ {added_count} websites blocked")
            elif current_language == 'zh':
                print(f"\n✓ 已拦截 {added_count} 个网站")
            else:
                print(f"\n✓ {added_count} Websites blockiert")
            flush_dns()
            return True
        else:
            if current_language == 'ru':
                print("⚠ Новые сайты не были добавлены (возможно, уже заблокированы)")
            elif current_language == 'en':
                print("⚠ No new websites added (possibly already blocked)")
            elif current_language == 'zh':
                print("⚠ 未添加新网站（可能已被拦截）")
            else:
                print("⚠ Keine neuen Websites hinzugefügt (möglicherweise bereits blockiert)")
            return False
            
    except Exception as e:
        if current_language == 'ru':
            print(f"✗ Ошибка при блокировке сайтов: {e}")
        elif current_language == 'en':
            print(f"✗ Website blocking error: {e}")
        elif current_language == 'zh':
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
            if current_language == 'ru':
                print("✓ Раздел DisallowRun удален из HKEY_LOCAL_MACHINE")
            elif current_language == 'en':
                print("✓ DisallowRun section removed from HKEY_LOCAL_MACHINE")
            elif current_language == 'zh':
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
                if current_language == 'ru':
                    print("✓ Раздел DisallowRun удален из HKEY_CURRENT_USER")
                elif current_language == 'en':
                    print("✓ DisallowRun section removed from HKEY_CURRENT_USER")
                elif current_language == 'zh':
                    print("✓ 已从HKEY_CURRENT_USER删除DisallowRun部分")
                else:
                    print("✓ DisallowRun-Bereich aus HKEY_CURRENT_USER entfernt")
            except:
                pass
        except:
            pass
        
        # Применяем изменения
        refresh_policy()
        
        if current_language == 'ru':
            print("✓ Все программы разблокированы!")
        elif current_language == 'en':
            print("✓ All programs unblocked!")
        elif current_language == 'zh':
            print("✓ 所有程序已解除拦截！")
        else:
            print("✓ Alle Programme freigeschaltet!")
        return True
        
    except Exception as e:
        if current_language == 'ru':
            print(f"✗ Ошибка при разблокировке: {e}")
        elif current_language == 'en':
            print(f"✗ Unblocking error: {e}")
        elif current_language == 'zh':
            print(f"✗ 解除拦截时出错：{e}")
        else:
            print(f"✗ Freischaltfehler: {e}")
        return False

def unblock_all_websites():
    """Разблокирует все сайты"""
    print(t('unblock_all_websites'))
    
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    backup_path = r"C:\Windows\System32\drivers\etc\hosts.backup"
    
    try:
        # Восстанавливаем из резервной копии
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, hosts_path)
            if current_language == 'ru':
                print("✓ Файл hosts восстановлен из резервной копии")
            elif current_language == 'en':
                print("✓ Hosts file restored from backup")
            elif current_language == 'zh':
                print("✓ hosts文件已从备份恢复")
            else:
                print("✓ Hosts-Datei aus Backup wiederhergestellt")
        else:
            # Удаляем наши блокировки из файла hosts
            with open(hosts_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Фильтруем строки, убирая наши блокировки
            blocker_header = "# === BLOCKED BY BARSIKYT BLOCKER ==="
            new_lines = []
            skip_mode = False
            
            for line in lines:
                if blocker_header in line:
                    skip_mode = True
                    continue
                if skip_mode and line.strip() and not line.startswith('#'):
                    continue
                if skip_mode and not line.strip():
                    skip_mode = False
                if not skip_mode:
                    new_lines.append(line)
            
            # Записываем обратно
            with open(hosts_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            
            if current_language == 'ru':
                print("✓ Блокировки сайтов удалены из файла hosts")
            elif current_language == 'en':
                print("✓ Website blocks removed from hosts file")
            elif current_language == 'zh':
                print("✓ 已从hosts文件删除网站拦截")
            else:
                print("✓ Website-Blockierungen aus Hosts-Datei entfernt")
        
        flush_dns()
        if current_language == 'ru':
            print("✓ Все сайты разблокированы!")
        elif current_language == 'en':
            print("✓ All websites unblocked!")
        elif current_language == 'zh':
            print("✓ 所有网站已解除拦截！")
        else:
            print("✓ Alle Websites freigeschaltet!")
        return True
        
    except Exception as e:
        if current_language == 'ru':
            print(f"✗ Ошибка при разблокировке сайтов: {e}")
        elif current_language == 'en':
            print(f"✗ Website unblocking error: {e}")
        elif current_language == 'zh':
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
            if current_language == 'ru':
                print("HKEY_LOCAL_MACHINE:")
            elif current_language == 'en':
                print("HKEY_LOCAL_MACHINE:")
            elif current_language == 'zh':
                print("HKEY_LOCAL_MACHINE：")
            else:
                print("HKEY_LOCAL_MACHINE:")
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    print(f"  {name}: {value}")
                    i += 1
                except WindowsError:
                    break
            total_blocks += i
            if i == 0:
                print(f"  {t('no_programs')}")
    except:
        if current_language == 'ru':
            print("HKEY_LOCAL_MACHINE: Не настроено")
        elif current_language == 'en':
            print("HKEY_LOCAL_MACHINE: Not configured")
        elif current_language == 'zh':
            print("HKEY_LOCAL_MACHINE：未配置")
        else:
            print("HKEY_LOCAL_MACHINE: Nicht konfiguriert")
    
    # Проверяем HKEY_CURRENT_USER
    try:
        user_disallow_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, user_disallow_path, 0, winreg.KEY_READ) as key:
            i = 0
            if current_language == 'ru':
                print("\nHKEY_CURRENT_USER:")
            elif current_language == 'en':
                print("\nHKEY_CURRENT_USER:")
            elif current_language == 'zh':
                print("\nHKEY_CURRENT_USER：")
            else:
                print("\nHKEY_CURRENT_USER:")
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    print(f"  {name}: {value}")
                    i += 1
                except WindowsError:
                    break
            total_blocks += i
            if i == 0:
                print(f"  {t('no_programs')}")
    except:
        if current_language == 'ru':
            print("HKEY_CURRENT_USER: Не настроено")
        elif current_language == 'en':
            print("HKEY_CURRENT_USER: Not configured")
        elif current_language == 'zh':
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
        if current_language == 'ru':
            print("\nНе удалось проверить статус политики")
        elif current_language == 'en':
            print("\nFailed to check policy status")
        elif current_language == 'zh':
            print("\n无法检查策略状态")
        else:
            print("\nKonnte Richtlinienstatus nicht überprüfen")
    
    # Показываем заблокированные сайты
    print("\n" + "="*50)
    print(t('blocked_sites'))
    try:
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        with open(hosts_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        blocker_header = "# === BLOCKED BY BARSIKYT BLOCKER ==="
        if blocker_header in content:
            lines = content.split('\n')
            site_count = 0
            in_blocked_section = False
            
            for line in lines:
                if blocker_header in line:
                    in_blocked_section = True
                    continue
                if in_blocked_section and line.strip() and not line.startswith('#'):
                    if '127.0.0.1' in line or '0.0.0.0' in line:
                        site = line.split()[-1]
                        print(f"  {site}")
                        site_count += 1
            
            if site_count == 0:
                print(f"  {t('no_sites')}")
            else:
                print(f"{t('total_site_blocks')} {site_count}")
        else:
            print(f"  {t('no_sites')}")
    except Exception as e:
        if current_language == 'ru':
            print(f"  Ошибка чтения файла hosts: {e}")
        elif current_language == 'en':
            print(f"  Hosts file read error: {e}")
        elif current_language == 'zh':
            print(f"  读取hosts文件时出错：{e}")
        else:
            print(f"  Hosts-Datei-Lesefehler: {e}")

def test_blocking():
    """Тестирование блокировки"""
    print(f"\n{t('testing_block')}")
    if current_language == 'ru':
        print("Попробуйте запустить заблокированную программу.")
        print("Если блокировка работает, вы увидите сообщение об ошибке.")
        input("Нажмите Enter после тестирования...")
    elif current_language == 'en':
        print("Try to run a blocked program.")
        print("If blocking works, you will see an error message.")
        input("Press Enter after testing...")
    elif current_language == 'zh':
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
    while True:
        site_input = input(t('enter_site')).strip()
        if not site_input:
            break
        
        # Обрабатываем ввод через запятую
        if ',' in site_input:
            sites = [s.strip() for s in site_input.split(',')]
            websites.extend(sites)
        else:
            websites.append(site_input)
    
    if websites:
        print(f"\n{t('will_block')} {', '.join(websites)}")
        confirm = input(t('continue_confirm')).lower()
        if confirm == 'y' or confirm == 'j':
            if block_websites(websites):
                print(f"✓ {t('sites_blocked')}")
                print(f"⚠ {t('browser_restart')}")
            else:
                if current_language == 'ru':
                    print("✗ Не удалось заблокировать сайты")
                elif current_language == 'en':
                    print("✗ Failed to block websites")
                elif current_language == 'zh':
                    print("✗ 无法拦截网站")
                else:
                    print("✗ Konnte Websites nicht blockieren")
    else:
        print(t('no_sites_entered'))

def change_language():
    """Смена языка интерфейса"""
    global current_language
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
        current_language = 'ru'
        print("✓ Язык изменен на русский")
    elif choice == '2':
        current_language = 'en'
        print("✓ Language changed to English")
    elif choice == '3':
        current_language = 'zh'
        print("✓ 语言已切换为中文")
    elif choice == '4':
        current_language = 'de'
        print("✓ Sprache auf Deutsch geändert")
    else:
        print(t('invalid_choice'))

def main():
    if not is_admin():
        run_as_admin()
        return
    
    global current_language
    
    while True:
        print_watermark()
        print(f" {t('admin_rights')}")
        print("="*55)
        print(f" {t('reboot_required')}")
        print("="*55)
        
        programs = {
            '1': {"name": t('programs')['1'], "executables": ["browser.exe", "yandex.exe"]},
            '2': {"name": t('programs')['2'], "executables": ["opera.exe"]},
            '3': {"name": t('programs')['3'], "executables": ["avastui.exe", "avast.exe", "avastsvchost.exe"]},
            '4': {"name": t('programs')['4'], "executables": ["360tray.exe", "360safe.exe", "360SD.exe"]},
            '5': {"name": t('programs')['5'], "executables": ["uTorrent.exe", "utorrent.exe"]},
            '6': {"name": t('programs')['6'], "executables": ["ccleaner.exe", "ccleaner64.exe"]},
            '7': {"name": t('programs')['7'], "executables": ["OneDrive.exe", "onedrive.exe", "OneDrive.Sync.Service.exe"]},
            '8': {"name": t('programs')['8'], "executables": ["max.exe", "Max.exe"]},
            '9': {"name": t('programs')['9'], "executables": ["mediaget.exe", "mgbot.exe"]},
            'ALL': {"name": t('programs')['ALL'], "executables": [
                "browser.exe", "yandex.exe", "opera.exe", "avastui.exe", "OneDrive.Sync.Service.exe",
                "360tray.exe", "uTorrent.exe", "ccleaner.exe", "onedrive.exe", "max.exe", "mediaget.exe", "avastsvchost.exe"
            ]}
        }

        website_presets = {
            '1': {"name": t('sites')['1'], "sites": ["yandex.ru", "ya.ru", "dzen.ru", "yandex.com", "yastatic.net"]},
            '2': {"name": t('sites')['2'], "sites": ["mail.ru", "mail.com"]},
            '3': {"name": t('sites')['3'], "sites": ["utorrent.ru", "utorrent.com"]},
            '4': {"name": t('sites')['4'], "sites": ["max.ru", "max.com"]}
        }

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
                if current_language == 'ru':
                    print(f"\nБудут заблокированы: {', '.join(program_info['executables'])}")
                elif current_language == 'en':
                    print(f"\nWill be blocked: {', '.join(program_info['executables'])}")
                elif current_language == 'zh':
                    print(f"\n将拦截：{', '.join(program_info['executables'])}")
                else:
                    print(f"\nWird blockiert: {', '.join(program_info['executables'])}")
                confirm = input(t('continue_confirm')).lower()
                if confirm == 'y' or confirm == 'j':
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
                    print(f"{key}. {preset['name']} - {', '.join(preset['sites'])}")
                
                preset_choice = input(t('choice'))
                if preset_choice in website_presets:
                    preset_info = website_presets[preset_choice]
                    print(f"\n{t('will_block')} {', '.join(preset_info['sites'])}")
                    confirm = input(t('continue_confirm')).lower()
                    if confirm == 'y' or confirm == 'j':
                        if block_websites(preset_info['sites']):
                            print(f"✓ {t('sites_blocked')}")
                else:
                    print(t('invalid_choice'))
                    
            elif site_choice == '2':
                custom_block_websites()

        elif choice == '3':
            confirm = input(f"{t('unblock_confirm')} ").lower()
            if confirm == 'y' or confirm == 'j':
                if unblock_all_programs():
                    if ask_reboot():
                        reboot_computer()

        elif choice == '4':
            confirm = input(f"{t('unblock_sites_confirm')} ").lower()
            if confirm == 'y' or confirm == 'j':
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

if __name__ == "__main__":
    main()