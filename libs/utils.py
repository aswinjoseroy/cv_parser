
def get_personal_elements_from_personal_info(personal_info_list):
    name = personal_info_list[0]
    email_ids = []
    address = ''
    for each in personal_info_list[1:]:
        each_parts = each.split("|")
        for each_part in each_parts:
            import re
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if re.search(regex, each_part.strip()):
                email_ids.append(each_part.strip())
            else:
                address = ''.join([address, each_part])
    return {"name": name, "email": "".join(email_ids), "address": address}
