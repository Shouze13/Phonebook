import json

class Contact:
    def __init__(self, last_name, first_name, middle_name, org_name, work_phone, personal_phone):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.org_name = org_name
        self.work_phone = work_phone
        self.personal_phone = personal_phone

    def __str__(self):
        return f"Фамилия: {self.last_name}\nИмя: {self.first_name}\nОтчество: {self.middle_name}\nОрганизация: {self.org_name}\nРабочий телефон: {self.work_phone}\nЛичный телефон: {self.personal_phone}"

class Phonebook:
    def __init__(self, file_name="phonebook.json"):
        self.file_name = file_name
        self.contacts = self.load_phonebook()

    def sort_phonebook(self):
        self.contacts = sorted(self.contacts, key=lambda contact: contact.last_name.lower())

    def load_phonebook(self):
        try:
            with open(self.file_name, 'r') as file:
                contacts_data = json.load(file)
                contacts = [Contact(**data) for data in contacts_data]
        except FileNotFoundError:
            contacts = []
        return contacts

    def save_phonebook(self):
        contacts_data = [{"first_name": contact.first_name,
                          "last_name": contact.last_name,
                          "middle_name": contact.middle_name,
                          "org_name": contact.org_name,
                          "work_phone": contact.work_phone,
                          "personal_phone": contact.personal_phone}
                         for contact in self.contacts]
        with open(self.file_name, 'w') as file:
            json.dump(contacts_data, file, indent=2)

    def display_contacts(self, page, contacts_per_page):
        start_idx = (page - 1) * contacts_per_page
        end_idx = start_idx + contacts_per_page

        for contact in self.contacts[start_idx:end_idx]:
            print(contact, '\n')

    def add_contact(self, contact):
        self.contacts.append(contact)
        self.save_phonebook()
        print("Контакт успешно добавлен.")

    def edit_contact(self, identifier, field, new_value):
        contact_found = False
        for contact in self.contacts:
            if contact.last_name.lower() == identifier.lower() or contact.work_phone == identifier:
                result = [contact for contact in self.contacts if contact.last_name.lower() == identifier.lower() or contact.work_phone == identifier]
                contact_found = True
                break
        if len(result) > 1:
            for i in result:
                print(i,'\n')
            contact = result[int(input("Найдено несколько контактов. Выберите необходимый:"))-1]
        if contact_found is True:
            setattr(contact, field, new_value)
            self.save_phonebook()
            print("Контакт успешно отредактирован.")
        else:
            print("Контакт не найден.")

    def search_contacts(self, criteria):
        if len(criteria) > 1:
            for i in criteria:
                results = [contact for contact in self.contacts if any(i.lower() in value.lower() for value in vars(contact).values())]
            return results
        else:
            criteria = ''.join(criteria)
            results = [contact for contact in self.contacts
                       if any(criteria.lower() in value.lower() for value in vars(contact).values())]
            return results

def main():
    phonebook = Phonebook()
    phonebook.sort_phonebook()
    while True:
        choice = input("\nВыберите действие:\n"
        "1. Вывод постранично записей из справочника\n"
        "2. Добавление новой записи в справочник\n"
        "3. Возможность редактирования записей в справочнике\n"
        "4. Поиск записей по одной или нескольким характеристикам\n"
        "0. Выход\n"
        "Ваш выбор: ")

        if choice == "1":
            page = int(input("Введите номер страницы: "))
            phonebook.display_contacts(page, contacts_per_page=2)
        elif choice == "2":
            last_name = input("Введите фамилию: ")
            first_name = input("Введите имя: ")
            middle_name = input("Введите отчество: ")
            org_name = input("Введите название организации: ")
            work_phone = input("Введите рабочий телефон: ")
            personal_phone = input("Введите личный телефон: ")
            new_contact = Contact(last_name, first_name, middle_name, org_name, work_phone, personal_phone)
            phonebook.add_contact(new_contact)
            phonebook.sort_phonebook()
        elif choice == "3":
            identifier = input("Введите фамилию или рабочий телефон контакта для редактирования: ")
            try:
                field = int(input("Введите номер поля для редактировния:\n"
                          "1 - Фамилия\n"
                          "2 - Имя\n"
                          "3 - Отчество\n"
                          "4 - Название организации\n"
                          "5 - Рабочий телефон\n"
                          "6 - Личный телефон\n"
                          "Ваш выбор: "))
                if field == 1:
                    field = "last_name"
                elif field == 2:
                    field = "first_name"
                elif field == 3:
                    field = "middle_name"
                elif field == 4:
                    field = "org_name"
                elif field == 5:
                    field = "work_phone"
                elif field == 6:
                    field = "personal_phone"
            except ValueError:
                print("Введите номер поля!!!")
                continue
            new_value = input("Введите новое значение: ")
            phonebook.edit_contact(identifier, field, new_value)
        elif choice == "4":
            search_criteria = input("Введите один или несколько известных параметров, разделённые запятой: ")
            results = phonebook.search_contacts(search_criteria.split(', '))
            print("Результаты поиска:")
            if len(results) == 0:
                print("Такого контакта не существует")
            else:
                for result in results:
                    print(result, '\n')
        elif choice == "0":
            print("Программа завершена.")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()