import requests
from bs4 import BeautifulSoup
import json
import sqlite3
import os.path
import re
from bs4.element import Comment
import urllib.parse


def creation_of_db():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    # con.commit()
    cur.execute("DROP TABLE info")
    cur.execute("DROP TABLE characteristics")
    cur.execute("DROP TABLE productLabels")
    cur.execute("DROP TABLE productFeatures")
    cur.execute("DROP TABLE benefitsDescriptionDescr")
    cur.execute("DROP TABLE benefitsDescriptionIcons")
    cur.execute("DROP TABLE subscriptionFee")
    cur.execute("DROP TABLE packages")
    cur.execute("DROP TABLE regulatorsOpIds")
    cur.execute("DROP TABLE regulators")
    cur.execute("DROP TABLE regOptionsId")
    cur.execute("DROP TABLE options")
    cur.execute("DROP TABLE opIdQuotas")
    cur.execute("DROP TABLE homeTariffs")
    cur.execute("DROP TABLE totalPrice")
    cur.execute("DROP TABLE connectionFee")
    cur.execute("DROP TABLE family")
    cur.execute("DROP TABLE parametrizedTariffSettings")
    cur.execute("DROP TABLE parametrizedOptions")
    cur.execute("DROP TABLE rangeSettings")
    cur.execute("DROP TABLE parametrizedOptionOptions")
    cur.execute("DROP TABLE coeffs")

    # cur.execute("DROP TABLE ")

    cur.execute("CREATE TABLE info(marketingId INTEGER PRIMARY KEY, id INTEGER, alias TEXT, title TEXT, \
                description TEXT, cardImageUrl TEXT, priority INTEGER, isPriorityProduct INTEGER, \
                 tariffType TEXT, isConfigurable INTEGER, isParameterizable INTEGER, isConvergent INTEGER)")
    # con.commit()

    cur.execute("CREATE TABLE characteristics(marketingId INTEGER, title TEXT, value TEXT, numValue TEXT, \
                 displayUnit TEXT, description TEXT, quotaUnit TEXT, isUnlimited INTEGER, numValueType TEXT, \
                 baseParameter TEXT, PRIMARY KEY(marketingId, baseParameter))")

    cur.execute(
        "CREATE TABLE productLabels(marketingId INTEGER, text TEXT, type TEXT, sortOrder INTEGER,\
        PRIMARY KEY(marketingId, text))")

    cur.execute(
        "CREATE TABLE productFeatures(marketingId INTEGER, title TEXT, value TEXT, \
        isUnlimited INTEGER, numValueType TEXT, \
        iconUrl TEXT, baseParameter TEXT, PRIMARY KEY (marketingId , title))")

    cur.execute("CREATE TABLE benefitsDescriptionDescr(marketingId INTEGER PRIMARY KEY, descr TEXT)")

    cur.execute(
        "CREATE TABLE benefitsDescriptionIcons(marketingId INTEGER, icon TEXT, PRIMARY KEY (marketingId, icon))")

    cur.execute("CREATE TABLE subscriptionFee(id INTEGER PRIMARY KEY, title TEXT, value TEXT, numValue INTEGER, \
                 displayUnit TEXT, quotaUnit TEXT, quotaPeriod TEXT, isUnlimited INTEGER, numValueType TEXT, \
                 sortOrder INTEGER, baseParameter TEXT)")

    cur.execute("CREATE TABLE packages(marketingId INTEGER, id INTEGER, PRIMARY KEY(marketingId, id))")

    cur.execute("CREATE TABLE regulatorsOpIds(id INTEGER, regulatorsOptionsId INTEGER, \
                PRIMARY KEY(id, regulatorsOptionsId))")

    cur.execute("CREATE TABLE regulators(regulatorsOptionsId INTEGER PRIMARY KEY, sortOrder INTEGER, quotaType TEXT)")

    cur.execute("CREATE TABLE regOptionsId(regulatorsOptionsId INTEGER, optionId INTEGER,\
                 PRIMARY KEY (regulatorsOptionsId, optionId))")

    cur.execute("CREATE TABLE options(optionId INTEGER PRIMARY KEY, label TEXT, valTitle TEXT, valValue TEXT, \
                valNumValue INTEGER, valDisplayUnit TEXT, valIsUnlimited INTEGER, valNumValueType TEXT, \
                valSortOrder INTEGER, valBaseParameter TEXT)")

    cur.execute("CREATE TABLE opIdQuotas(optionId INTEGER, title TEXT, value TEXT, displayUnit TEXT, quotaUnit TEXT, \
                isUnlimited INTEGER, numValueType TEXT, sortOrder INTEGER, baseParameter TEXT, \
                PRIMARY KEY(optionId, baseParameter))")

    cur.execute("CREATE TABLE homeTariffs(marketingId INTEGER, id INTEGER, title TEXT, description TEXT, alias TEXT, \
                htorder INTEGER, phoneTariff INTEGER, bigListImageHero1 TEXT, bigListImageHero2 TEXT, cardImageUrl TEXT, \
                PRIMARY KEY(marketingId, id))")

    cur.execute("CREATE TABLE totalPrice(tariffId INTEGER PRIMARY KEY, valueFormat TEXT, value TEXT, unitDisplay TEXT, \
                unitPeriodDisplay TEXT, unitPeriodMultiplier INTEGER, uUnitDisplay TEXT, unitQuotaPeriod TEXT)")

    cur.execute("CREATE TABLE connectionFee(id INTEGER PRIMARY KEY, valueFormat TEXT, value TEXT, unitDisplay TEXT, \
                unitPeriodMultiplier INTEGER, uUnitDisplay TEXT)")

    cur.execute("CREATE TABLE family(tariffId INTEGER, id INTEGER, title TEXT, alias TEXT, hasFamilyCard INTEGER, \
                PRIMARY KEY(tariffId, id))")

    cur.execute("CREATE TABLE parametrizedTariffSettings(marketingId INTEGER PRIMARY KEY, defaultPrice REAL)")

    cur.execute("CREATE TABLE parametrizedOptions(marketingId INTEGER, id INTEGER, serviceType TEXT, \
                sortOrder INTEGER, PRIMARY KEY(marketingId, id))")

    cur.execute("CREATE TABLE rangeSettings(paramOpId INTEGER, defaultValue REAL, defaultValueForAuthorized REAL, \
                minValue REAL, maxValue REAL, step REAL, isValid INTEGER)")

    cur.execute("CREATE TABLE parametrizedOptionOptions(marketingId INTEGER, id INTEGER, title TEXT, \
                isDefault INTEGER, PRIMARY KEY(marketingId, id))")

    cur.execute("CREATE TABLE coeffs(marketingId INTEGER PRIMARY KEY, useForMinutesPackage REAL, \
                regional REAL, useForInternetPackage REAL, useForMessagesPackage REAL, additional INTEGER)")

    con.commit()


def extract_keys(json_data):
    keys = []
    for key, value in json_data.items():
        keys.append(key)
    # print(keys)
    return keys


def bool_to_int(some_bool):
    return 1 if some_bool == "True" else 0


def type_to_bool(tariff, param):
    try:
        return 1 if tariff[param] else 0
    except KeyError:
        return 0


def not_in_keys(json_obj, keys_needed):
    keys = extract_keys(json_obj)
    inds = []
    for i in range(len(keys_needed)):
        key = keys_needed[i]
        if key not in keys:
            inds.append(i)
    return inds


def fill_with_nones(json_obj, keys, parent_json_obj=None, parent_obj_param=None):
    if parent_json_obj:
        print(extract_keys(json_obj))
        print(keys)
        nones_inds = not_in_keys(json_obj, keys)
        print(nones_inds)
        data = [None] * (len(keys) + 1)
        for i in range(len(keys) + 1):
            if i == 0:
                data[0] = parent_json_obj[parent_obj_param]
                print(data)
            elif (i - 1) not in nones_inds:
                data[i] = json_obj[keys[i - 1]]
                print(data)
    else:
        nones_inds = not_in_keys(json_obj, keys)
        data = [None] * len(keys)
        # print(len(data))
        for i in range(len(keys)):
            if i not in nones_inds:
                # print(i)
                data[i] = json_obj[keys[i]]
    return data


def insert_all_characteristics(cursor, json_obj):
    for each in json_obj['productCharacteristics']:
        # print(tariff['productCharacteristics'][j])
        #
        # print(extract_keys(each))
        keys = ['title', 'value', 'numValue', 'displayUnit', 'description', 'quotaUnit',
                'isUnlimited', 'numValueType', 'baseParameter']
        data = fill_with_nones(each, keys, json_obj, 'marketingId')
        cursor.execute(f"INSERT INTO characteristics VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)


def insert_all_product_labels(cursor, json_obj):
    for each in json_obj['productLabels']:
        keys = ['text', 'type', 'sortOrder']
        data = fill_with_nones(each, keys, json_obj, 'marketingId')
        cursor.execute(
            f"INSERT INTO productLabels VALUES(?, ?, ?, ?)", data)


def insert_all_benefits_description_icons(cursor, json_obj):
    for img in json_obj['benefitsDescription']['icons']:
        data = [json_obj['marketingId'], img]
        cursor.execute("INSERT INTO benefitsDescriptionIcons VALUES(?, ?)", data)


def insert_all_product_features(cursor, json_obj):
    for each in json_obj['productFeatures']:
        keys = ['title', 'value', 'isUnlimited', 'numValueType', 'iconUrl', 'baseParameter']
        data = fill_with_nones(each, keys, json_obj, 'marketingId')
        cursor.execute("INSERT INTO productFeatures VALUES(?, ?, ?, ?, ?, ?, ?)", data)


def insert_subscription_fee(cursor, json_obj):
    keys = ['title', 'value', 'numValue', 'displayUnit', 'quotaUnit', 'quotaPeriod',
            'isUnlimited', 'numValueType', 'sortOrder', 'baseParameter']
    data = fill_with_nones(json_obj['subscriptionFee'], keys, json_obj, 'id')
    cursor.execute("INSERT INTO subscriptionFee VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)


def insert_all_configurable_tariff_settings(cursor, json_obj):
    for i in json_obj['configurableTariffSettings']['packages']:
        data = [json_obj['marketingId'], i['id']]
        cursor.execute("INSERT INTO packages VALUES(?, ?)", data)

        # insert all regulatorsOptionsIds
        for roi in i['regulatorsOptionsIds']:
            data = [i['id'], roi]
            cursor.execute("INSERT INTO regulatorsOpIds VALUES(?, ?)", data)

        insert_subscription_fee(cursor, i)


def insert_all_reg_quotas(cursor, json_obj):
    for quota in json_obj['quotas']:
        keys = ['title', 'value', 'displayUnit', 'quotaUnit', 'isUnlimited',
                'numValueType', 'sortOrder', 'baseParameter']
        data = fill_with_nones(quota, keys, json_obj, 'optionId')
        cursor.execute("INSERT INTO opIdQuotas VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", data)


def insert_option(cursor, json_obj):
    keys = ['title', 'value', 'numValue', 'displayUnit', 'isUnlimited',
            'numValueType', 'sortOrder', 'baseParameter']
    data = [json_obj['optionId'], json_obj['label']]
    data += fill_with_nones(json_obj['value'], keys)
    cursor.execute("INSERT INTO options VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)


def insert_all_regulators_of_configurable_tariff_settings(cursor, json_obj):
    for regs in json_obj['configurableTariffSettings']['regulators']:

        data = [regs['id'], regs['sortOrder'], regs['quotaType']]
        cursor.execute("INSERT INTO regulators VALUES(?, ?, ?)", data)

        insert_all_regs_options(cursor, regs)


def insert_all_regs_options(cursor, json_obj):
    for ops in json_obj['options']:
        data = [json_obj['id'], ops['optionId']]
        cursor.execute("INSERT INTO regOptionsId VALUES(?, ?)", data)

        insert_option(cursor, ops)
        insert_all_reg_quotas(cursor, ops)


def insert_formula_coefficients(cursor, json_obj):
    keys = ['useForMinutesPackage', 'regional', 'useForInternetPackage',
            'useForMessagesPackage', 'additional']
    data = fill_with_nones(json_obj['parametrizedTariffSettings']['formulaCoefficients'], keys, json_obj,
                           'marketingId')
    cursor.execute("INSERT INTO coeffs VALUES(?, ?, ?, ?, ?, ?)", data)


def insert_all_parametrized_options_with_settings(cursor, json_obj):
    for parOption in json_obj['parametrizedTariffSettings']['parametrizedOptions']:
        keys = ['id', 'serviceType', 'sortOrder']
        data = fill_with_nones(parOption, keys, json_obj, 'marketingId')
        cursor.execute("INSERT INTO parametrizedOptions VALUES(?, ?, ?, ?)", data)

        keys = ['defaultValue', 'defaultValueForAuthorized', 'minValue', 'maxValue', 'step', 'isValid']
        data = fill_with_nones(parOption['rangeSettings'], keys, parOption, 'id')
        cursor.execute("INSERT INTO rangeSettings VALUES(?, ?, ?, ?, ?, ?, ?)", data)


def insert_all_option_options(cursor, json_obj):
    for option in json_obj['parametrizedTariffSettings']['options']:
        keys = ['id', 'title', 'isDefault']
        data = fill_with_nones(option, keys, json_obj, 'marketingId')
        cursor.execute("INSERT INTO parametrizedOptionOptions VALUES(?, ?, ?, ?)", data)


def insert_total_price(cursor, json_obj):
    keys = ['valueFormat', 'value', 'unitDisplay', 'unitPeriodDisplay',
            'unitPeriodMultiplier', 'uUnitDisplay', 'unitQuotaPeriod']
    data = fill_with_nones(json_obj['totalPrice'], keys, json_obj, 'id')
    cursor.execute("INSERT INTO totalPrice VALUES(?, ?, ?, ?, ?, ?, ?, ?)", data)


def insert_connection_fee(cursor, json_obj):
    keys = ['valueFormat', 'value', 'unitDisplay', 'unitPeriodMultiplier', 'uUnitDisplay']
    data = fill_with_nones(json_obj['connectionFee'], keys, json_obj, 'id')
    cursor.execute("INSERT INTO connectionFee VALUES(?, ?, ?, ?, ?, ?)", data)


def insert_family(cursor, json_obj):
    keys = ['id', 'title', 'alias', 'hasFamilyCard']
    data = fill_with_nones(json_obj['family'], keys, json_obj, 'id')
    cursor.execute("INSERT INTO family VALUES(?, ?, ?, ?, ?)", data)


def insert_all_home_tariff_settings(cursor, json_obj):
    for each in json_obj['homeTariffSettings']['familyOffers']:
        keys = ['id', 'title', 'description', 'alias', 'order', 'phoneTariffId',
                'bigListImageHero1', 'bigListImageHero2', 'cardImageUrl']
        data = fill_with_nones(each, keys, json_obj, 'marketingId')
        cursor.execute("INSERT INTO homeTariffs VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)

        insert_total_price(cursor, each)
        # keys = ['valueFormat', 'value', 'unitDisplay', 'unitPeriodDisplay',
        #         'unitPeriodMultiplier', 'uUnitDisplay', 'unitQuotaPeriod']
        # data = fill_with_nones(each['totalPrice'], keys, each, 'id')
        # cur.execute("INSERT INTO totalPrice VALUES(?, ?, ?, ?, ?, ?, ?, ?)", data)

        insert_connection_fee(cursor, each)
        # keys = ['valueFormat', 'value', 'unitDisplay', 'unitPeriodMultiplier', 'uUnitDisplay']
        # data = fill_with_nones(each['connectionFee'], keys, each, 'id')
        # cur.execute("INSERT INTO connectionFee VALUES(?, ?, ?, ?, ?, ?)", data)

        insert_family(cursor, each)
        # keys = ['id', 'title', 'alias', 'hasFamilyCard']
        # data = fill_with_nones(each['family'], keys, each, 'id')
        # cur.execute("INSERT INTO family VALUES(?, ?, ?, ?, ?)", data)


def insert_main_info(cursor, json_obj):
    data = []
    keys = ['marketingId', 'id', 'alias', 'title', 'description',
            'cardImageUrl', 'priority', 'isPriorityProduct', 'tariffType']
    data += fill_with_nones(json_obj, keys)
    data.append(type_to_bool(json_obj, 'configurableTariffSettings'))
    data.append(type_to_bool(json_obj, 'parametrizedTariffSettings'))
    data.append(type_to_bool(json_obj, 'convergentTariffSettings'))
    cursor.execute("INSERT INTO info VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    return data


def store_item(tariff):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()

        data1 = insert_main_info(cur, tariff)
        # keys = ['marketingId', 'id', 'alias', 'title', 'description',
        #         'cardImageUrl', 'priority', 'isPriorityProduct', 'tariffType']
        # data1 += fill_with_nones(tariff, keys)
        # data1.append(type_to_bool(tariff, 'configurableTariffSettings'))
        # data1.append(type_to_bool(tariff, 'parametrizedTariffSettings'))
        # data1.append(type_to_bool(tariff, 'convergentTariffSettings'))
        # print(data1)
        # cur.execute("INSERT INTO info VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data1)

        # print(tariff['productCharacteristics'][0]['quotaUnit'])
        # j = 0
        print(tariff['tariffType'])
        if tariff['tariffType'] == "HomeServicesTariff":
            insert_all_home_tariff_settings(cur, tariff)
            # for each in tariff['homeTariffSettings']['familyOffers']:
            #     keys = ['id', 'title', 'description', 'alias', 'order', 'phoneTariffId',
            #             'bigListImageHero1', 'bigListImageHero2', 'cardImageUrl']
            #     data = fill_with_nones(each, keys, tariff, 'marketingId')
            #     cur.execute("INSERT INTO homeTariffs VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
            #
            #     keys = ['valueFormat', 'value', 'unitDisplay', 'unitPeriodDisplay',
            #             'unitPeriodMultiplier', 'uUnitDisplay', 'unitQuotaPeriod']
            #     data = fill_with_nones(each['totalPrice'], keys, each, 'id')
            #     cur.execute("INSERT INTO totalPrice VALUES(?, ?, ?, ?, ?, ?, ?, ?)", data)
            #
            #     keys = ['valueFormat', 'value', 'unitDisplay', 'unitPeriodMultiplier', 'uUnitDisplay']
            #     data = fill_with_nones(each['connectionFee'], keys, each, 'id')
            #     cur.execute("INSERT INTO connectionFee VALUES(?, ?, ?, ?, ?, ?)", data)
            #
            #     keys = ['id', 'title', 'alias', 'hasFamilyCard']
            #     data = fill_with_nones(each['family'], keys, each, 'id')
            #     cur.execute("INSERT INTO family VALUES(?, ?, ?, ?, ?)", data)
        # elif data1[-1] == 1:

        else:
            insert_all_product_labels(cur, tariff)
            # for each in tariff['productLabels']:
            #     keys = ['text', 'type', 'sortOrder']
            #     data = fill_with_nones(each, keys, tariff, 'marketingId')
            #     cur.execute(
            #         f"INSERT INTO productLabels VALUES(?, ?, ?, ?)", data)

            data = [tariff['marketingId'], tariff['benefitsDescription']['description']]
            cur.execute(f"INSERT INTO benefitsDescriptionDescr VALUES(?, ?)", data)

            insert_all_benefits_description_icons(cur, tariff)
            # for img in tariff['benefitsDescription']['icons']:
            #     data = [tariff['marketingId'], img]
            #     cur.execute("INSERT INTO benefitsDescriptionIcons VALUES(?, ?)", data)
            if data1[-2] == 0:
                insert_all_characteristics(cur, tariff)
                # for each in tariff['productCharacteristics']:
                #     # print(tariff['productCharacteristics'][j])
                #     #
                #     # print(extract_keys(each))
                #     keys = ['title', 'value', 'numValue', 'displayUnit', 'description', 'quotaUnit',
                #             'isUnlimited', 'numValueType', 'baseParameter']
                #     data = fill_with_nones(each, keys, tariff, 'marketingId')
                #     cur.execute(f"INSERT INTO characteristics VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)

                insert_all_product_features(cur, tariff)
                # for each in tariff['productFeatures']:
                #     keys = ['title', 'value', 'isUnlimited', 'numValueType', 'iconUrl', 'baseParameter']
                #     data = fill_with_nones(each, keys, tariff, 'marketingId')
                #     cur.execute("INSERT INTO productFeatures VALUES(?, ?, ?, ?, ?, ?, ?)", data)

                if data1[-3] == 0:
                    data = [tariff['marketingId'], tariff['id']]
                    cur.execute("INSERT INTO packages VALUES(?, ?)", data)
                    # print(tariff['subscriptionFee'])

                    insert_subscription_fee(cur, tariff)
                    # keys = ['title', 'value', 'numValue', 'displayUnit', 'quotaUnit', 'quotaPeriod',
                    #         'isUnlimited', 'numValueType', 'sortOrder', 'baseParameter']
                    # data = fill_with_nones(tariff['subscriptionFee'], keys, tariff, 'id')
                    # cur.execute("INSERT INTO subscriptionFee VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
                else:
                    insert_all_configurable_tariff_settings(cur, tariff)
                    # for i in tariff['configurableTariffSettings']['packages']:
                    #     data = [tariff['marketingId'], i['id']]
                    #     cur.execute("INSERT INTO packages VALUES(?, ?)", data)
                    #     for roi in i['regulatorsOptionsIds']:
                    #         data = [i['id'], roi]
                    #         cur.execute("INSERT INTO regulatorsOpIds VALUES(?, ?)", data)
                    #
                    #     insert_subscription_fee(cur, i)
                    # keys = ['title', 'value', 'numValue', 'displayUnit', 'quotaUnit', 'quotaPeriod',
                    #         'isUnlimited', 'numValueType', 'sortOrder', 'baseParameter']
                    # data = fill_with_nones(i['subscriptionFee'], keys, i, 'id')
                    # cur.execute("INSERT INTO subscriptionFee VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)

                    insert_all_regulators_of_configurable_tariff_settings(cur, tariff)
                    # for regs in tariff['configurableTariffSettings']['regulators']:
                    #     data = [regs['id'], regs['sortOrder'], regs['quotaType']]
                    #     cur.execute("INSERT INTO regulators VALUES(?, ?, ?)", data)
                    #
                    #     for ops in regs['options']:
                    #         data = [regs['id'], ops['optionId']]
                    #         cur.execute("INSERT INTO regOptionsId VALUES(?, ?)", data)
                    #
                    #         keys = ['title', 'value', 'numValue', 'displayUnit', 'isUnlimited',
                    #                 'numValueType', 'sortOrder', 'baseParameter']
                    #         data = [ops['optionId'], ops['label']]
                    #         data += fill_with_nones(ops['value'], keys)
                    #         cur.execute("INSERT INTO options VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
                    #
                    #         insert_all_reg_quotas(cur, ops)
                    # for quota in ops['quotas']:
                    #     keys = ['title', 'value', 'displayUnit', 'quotaUnit', 'isUnlimited',
                    #             'numValueType', 'sortOrder', 'baseParameter']
                    #     data = fill_with_nones(quota, keys, ops, 'optionId')
                    #     cur.execute("INSERT INTO opIdQuotas VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
            else:
                data = [tariff['marketingId'], tariff['parametrizedTariffSettings']['defaultPackagePrice']]
                cur.execute("INSERT INTO parametrizedTariffSettings VALUES(?, ?)", data)

                insert_formula_coefficients(cur, tariff)
                # keys = ['useForMinutesPackage', 'regional', 'useForInternetPackage',
                #         'useForMessagesPackage', 'additional']
                # data = fill_with_nones(tariff['parametrizedTariffSettings']['formulaCoefficients'], keys, tariff,
                #                        'marketingId')
                # cur.execute("INSERT INTO coeffs VALUES(?, ?, ?, ?, ?, ?)", data)

                insert_all_parametrized_options_with_settings(cur, tariff)
                # for parOption in tariff['parametrizedTariffSettings']['parametrizedOptions']:
                #     keys = ['id', 'serviceType', 'sortOrder']
                #     data = fill_with_nones(parOption, keys, tariff, 'marketingId')
                #     cur.execute("INSERT INTO parametrizedOptions VALUES(?, ?, ?, ?)", data)
                #
                #     keys = ['defaultValue', 'defaultValueForAuthorized', 'minValue', 'maxValue', 'step', 'isValid']
                #     data = fill_with_nones(parOption['rangeSettings'], keys, parOption, 'id')
                #     cur.execute("INSERT INTO rangeSettings VALUES(?, ?, ?, ?, ?, ?, ?)", data)

                insert_all_option_options(cur, tariff)
                # for option in tariff['parametrizedTariffSettings']['options']:
                #     keys = ['id', 'title', 'isDefault']
                #     data = fill_with_nones(option, keys, tariff, 'marketingId')
                #     cur.execute("INSERT INTO parametrizedOptionOptions VALUES(?, ?, ?, ?)", data)

        con.commit()


def extract_items(json_data):
    # extract_keys(json_data)
    tariffs = json_data['actualTariffs']
    # print(tariffs)
    i = 0
    for tariff in tariffs:
        # if i <= 1:
        #     print(tariff)
        # elif i == 0:
        #     i += 1
        print(tariff, "\n")
        store_item(tariff)

        # if i ==0:
        #     keys = ['marketingId', 'id', 'alias', 'title', 'description',
        #             'cardImageUrl', 'priority', 'isPriorityProduct', 'tariffType']
        #     print(fill_with_nones(tariff, keys))
    # tariffs = []
    # for tariff in catalog:

    # extract_keys(catalog)
    # print(catalog[0]['marketingId'])


def parse():
    doc = requests.get("https://moskva.mts.ru/personal/mobilnaya-svyaz/tarifi/vse-tarifi/mobile-tv-inet")
    soup = BeautifulSoup(doc.content, 'html.parser')
    scripts = soup.findAll("script")
    for each in scripts:
        try:
            if "window.globalSettings.tariffs" in each.string:
                json_value = '{%s}' % (each.string.partition('{')[2].rpartition('}')[0],)
                value = json.loads(json_value)
                # print(value)
                return value

        except Exception:
            continue


if __name__ == "__main__":
    creation_of_db()
    parsed_json = parse()
    # print(parsed_json)
    extract_items(parsed_json)
