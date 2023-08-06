import requests
import json


def get_package_list(branch):
    url = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"
    response = requests.get(url)
    package_list = json.loads(response.text)
    return package_list['packages']


def compare_packages(branch1, branch2):
    package_list_1 = get_package_list(branch1)
    package_list_2 = get_package_list(branch2)
    # Создаем словари для хранения списков пакетов
    package_dict_1 = {}
    package_dict_2 = {}
    for package in package_list_1:
        package_dict_1.setdefault(package['arch'], {})[package['name']] = package
    for package in package_list_2:
        package_dict_2.setdefault(package['arch'], {})[package['name']] = package

    # Находим все пакеты, которые есть только в первой ветке
    only_in_1 = {}
    for arch in package_dict_1:
        only_in_1[arch] = []
        for package_name in package_dict_1[arch]:
            if package_name not in package_dict_2.get(arch, {}):
                only_in_1[arch].append(package_dict_1[arch][package_name])

    # Находим все пакеты, которые есть только во второй ветке
    only_in_2 = {}
    for arch in package_dict_2:
        only_in_2[arch] = []
        for package_name in package_dict_2[arch]:
            if package_name not in package_dict_1.get(arch, {}):
                only_in_2[arch].append(package_dict_2[arch][package_name])

    # Находим все пакеты, version-release которых больше в первой ветке, чем во второй
    greater_in_1 = {}
    for arch in package_dict_1:
        greater_in_1[arch] = []
        for package_name in package_dict_1[arch]:
            if package_name in package_dict_2.get(arch, {}):
                if package_dict_1[arch][package_name]['version'] > package_dict_2[arch][package_name]['version'] or (package_dict_1[arch][package_name]['version'] == package_dict_2[arch][package_name]['version'] and package_dict_1[arch][package_name]['release'] > package_dict_2[arch][package_name]['release']):
                    greater_in_1[arch].append(package_dict_1[arch][package_name])


    # Создаем словарь с результатами сравнения
    result = {
        "only_in_1": only_in_1,
        "only_in_2": only_in_2,
        "greater_in_1": greater_in_1
    }

    # Возвращаем результат
    return (json.dumps(result, indent=4))

