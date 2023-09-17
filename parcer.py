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
    cur.execute("DROP TABLE tvPackage")
    cur.execute("DROP TABLE devices")
    cur.execute("DROP TABLE tariffDevices")
    cur.execute("DROP TABLE rentPrice")
    cur.execute("DROP TABLE salePrice")
    cur.execute("DROP TABLE actions")
    cur.execute("DROP TABLE tariffActions")

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

    cur.execute("CREATE TABLE regulators(regulatorsOptionsId INTEGER PRIMARY KEY, marketingId INTEGER, \
                sortOrder INTEGER, quotaType TEXT)")

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
                unitPeriodDisplay TEXT, unitPeriodMultiplier INTEGER, \
                uUnitDisplay TEXT, unitQuotaPeriod TEXT)")

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

    cur.execute("CREATE TABLE tvPackage(marketingId INTEGER PRIMARY KEY, id INTEGER, alias TEXT, isSatellite INTEGER, isIpTv INTEGER, \
                isIpTv2 INTEGER, isDvbc INTEGER, isBase INTEGER, titleForSite TEXT, channelsHdCount INTEGER, \
                channelsUhdCount INTEGER, channelsCount INTEGER, forDTV INTEGER, forInteractiveTv INTEGER, \
                external INTEGER)")

    cur.execute("CREATE TABLE devices(id INTEGER PRIMARY KEY, archive INTEGER, forInteractiveTv INTEGER, \
                isInternet INTEGER, isMandatory INTEGER, isOverrideRentPrice INTEGER, isPhone INTEGER, isTv INTEGER, \
                isCctv INTEGER, rentUnavailable INTEGER, \
                saleUnavailable INTEGER, title TEXT, sortOrder INTEGER, rentPriceId INTEGER, salePriceId INTEGER)")

    cur.execute("CREATE TABLE tariffDevices(marketingId INTEGER, deviceId INTEGER, PRIMARY KEY(marketingId, deviceId))")

    cur.execute("CREATE TABLE rentPrice(id INTEGER PRIMARY KEY, valueFormat TEXT, value REAL, \
                unitDisplay TEXT, unitPeriodDisplay TEXT, unitPeriodMultiplier INTEGER, \
                uUnitDisplay TEXT, unitQuotaPeriod TEXT)")

    cur.execute("CREATE TABLE salePrice(id INTEGER PRIMARY KEY, valueFormat TEXT, value REAL, \
                unitDisplay TEXT, unitPeriodDisplay TEXT, unitPeriodMultiplier INTEGER, \
                uUnitDisplay TEXT, unitQuotaPeriod TEXT)")

    cur.execute("CREATE TABLE actions(id INTEGER PRIMARY KEY, title TEXT, promoPeriod TEXT, isArchive INTEGER, \
                discountAbsolute REAL, isDefault INTEGER, isHidden INTEGER, highlightAfterPromo INTEGER, \
                isApplied INTEGER)")

    cur.execute("CREATE TABLE tariffActions(marketingId INTEGER, actionId INTEGER, PRIMARY KEY(marketingId, actionId))")

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


def insert_benefits_description(cursor, json_obj):
    data = [json_obj['marketingId'], json_obj['benefitsDescription']['description']]
    cursor.execute(f"INSERT INTO benefitsDescriptionDescr VALUES(?, ?)", data)

    insert_all_benefits_description_icons(cursor, json_obj)


def insert_all_product_features(cursor, json_obj):
    for each in json_obj['productFeatures']:
        keys = ['title', 'value', 'isUnlimited', 'numValueType', 'iconUrl', 'baseParameter']
        data = fill_with_nones(each, keys, json_obj, 'marketingId')
        cursor.execute("INSERT INTO productFeatures VALUES(?, ?, ?, ?, ?, ?, ?)", data)


def insert_subscription_fee(cursor, json_obj, id_key):
    keys = ['title', 'value', 'numValue', 'displayUnit', 'quotaUnit', 'quotaPeriod',
            'isUnlimited', 'numValueType', 'sortOrder', 'baseParameter']
    data = fill_with_nones(json_obj['subscriptionFee'], keys, json_obj, id_key)
    cursor.execute("INSERT INTO subscriptionFee VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)


def insert_all_configurable_tariff_settings(cursor, json_obj):
    for i in json_obj['configurableTariffSettings']['packages']:
        data = [json_obj['marketingId'], i['id']]
        cursor.execute("INSERT INTO packages VALUES(?, ?)", data)

        # insert all regulatorsOptionsIds
        for roi in i['regulatorsOptionsIds']:
            data = [i['id'], roi]
            cursor.execute("INSERT INTO regulatorsOpIds VALUES(?, ?)", data)

        insert_subscription_fee(cursor, i, 'id')


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
        data = [regs['id'], json_obj['marketingId'], regs['sortOrder'], regs['quotaType']]
        cursor.execute("INSERT INTO regulators VALUES(?, ?, ?, ?)", data)

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
    keys = ['valueFormat', 'value']
    data = fill_with_nones(json_obj['totalPrice'], keys, json_obj, 'id')
    data += collect_unit_fields(json_obj['totalPrice'])
    cursor.execute("INSERT INTO totalPrice VALUES(?, ?, ?, ?, ?, ?, ?, ?)", data)


def insert_connection_fee(cursor, json_obj):
    keys = ['valueFormat', 'value']
    data = fill_with_nones(json_obj['connectionFee'], keys, json_obj, 'id')
    data += collect_unit_fields(json_obj['connectionFee'])
    cursor.execute("INSERT INTO connectionFee VALUES(?, ?, ?, ?, ?, ?, ?, ?)", data)


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

        try:
            insert_connection_fee(cursor, each)
        except KeyError:
            True
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


def insert_tv_package(cursor, json_obj):  # json is tariff
    keys = ['id', 'alias', 'isSatellite', 'isIpTv', 'isIpTv2', 'isDvbc', 'isBase', 'titleForSite', 'channelsHdCount',
            'channelsUhdCount', 'channelsCount', 'forDTV', 'forInteractiveTv', 'external']
    data = fill_with_nones(json_obj['convergentTariffSettings']['offer']['tvPackage'], keys, json_obj, 'marketingId')
    cursor.execute("INSERT INTO tvPackage VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)


def collect_unit_fields(json_obj):
    keys = ['display', 'periodDisplay', 'periodMultiplier', 'unitDisplay', 'quotaPeriod']
    return fill_with_nones(json_obj['unit'], keys)


def insert_rent_price_and_return_id(cursor, json_obj):
    keys = ['valueFormat', 'value']
    data = fill_with_nones(json_obj['rentPrice'], keys)
    data += collect_unit_fields(json_obj['rentPrice'])
    cursor.execute("INSERT INTO rentPrice(valueFormat, value, \
                unitDisplay, unitPeriodDisplay, unitPeriodMultiplier, \
                uUnitDisplay, unitQuotaPeriod) VALUES(?, ?, ?, ?, ?, ?, ?)", data)
    return cursor.lastrowid


def insert_sale_price_and_return_id(cursor, json_obj):
    keys = ['valueFormat', 'value']

    data = fill_with_nones(json_obj['salePrice'], keys)
    data += collect_unit_fields(json_obj['salePrice'])
    cursor.execute("INSERT INTO salePrice(valueFormat, value, \
                unitDisplay, unitPeriodDisplay, unitPeriodMultiplier, \
                uUnitDisplay, unitQuotaPeriod) VALUES(?, ?, ?, ?, ?, ?, ?)", data)
    return cursor.lastrowid


def insert_all_tariff_devices_with_prices(cursor, json_obj):
    for device in json_obj['convergentTariffSettings']['offer']['devices']:
        rent_price_id = insert_rent_price_and_return_id(cursor, device)
        try:
            sale_price_id = insert_sale_price_and_return_id(cursor, device)
        except KeyError:
            sale_price_id = None
        keys = ['archive', 'forInteractiveTv', 'isInternet', 'isMandatory', 'isOverrideRentPrice', 'isPhone', 'isTv',
                'isCctv', 'rentUnavailable', 'saleUnavailable', 'title', 'sortOrder']
        data = []
        data += fill_with_nones(device, keys)
        data.append(rent_price_id)
        data.append(sale_price_id)
        # print(len(data))
        cursor.execute("INSERT INTO devices(archive, forInteractiveTv, \
                isInternet, isMandatory, isOverrideRentPrice, isPhone, isTv, \
                isCctv, rentUnavailable, \
                saleUnavailable, title, sortOrder, rentPriceId, salePriceId) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       data)

        id = cursor.lastrowid
        cursor.execute("INSERT INTO tariffDevices VALUES(?, ?)", (json_obj['marketingId'], id))


def insert_action_return_id(cursor, json_obj):
    keys = ['id', 'title', 'promoPeriod', 'isArchive', 'discountAbsolute', 'isDefault',
            'isHidden', 'hihglightAfterPromo', 'isApplied']
    data = []
    data += fill_with_nones(json_obj, keys)
    cursor.execute("INSERT OR IGNORE INTO actions VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    return data[0]


def insert_all_tariff_actions(cursor, json_obj):
    for action in json_obj['convergentTariffSettings']['offer']['actions']:
        action_id = insert_action_return_id(cursor, action)
        cursor.execute("INSERT INTO tariffActions VALUES(?, ?)", (json_obj['marketingId'], action_id))


def store_item(tariff):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        data1 = insert_main_info(cur, tariff)

        # print(tariff['productCharacteristics'][0]['quotaUnit'])
        print(tariff['tariffType'])
        if tariff['tariffType'] == "HomeServicesTariff":
            insert_all_home_tariff_settings(cur, tariff)
        elif data1[-1] == 1:  # inserting all convergent tariff params
            insert_all_characteristics(cur, tariff)

            insert_all_product_features(cur, tariff)

            # print(tariff['benefitsDescription'])

            try:
                insert_benefits_description(cur, tariff)
            except KeyError:
                True
            insert_subscription_fee(cur, tariff, 'marketingId')
            try:
                insert_tv_package(cur, tariff)
            except KeyError:
                True

            insert_all_tariff_devices_with_prices(cur, tariff)

            insert_all_tariff_actions(cur, tariff)
        else:  # parametried or configurable or ordinary
            try:
                insert_all_product_labels(cur, tariff)
            except KeyError:
                True
            try:
                insert_benefits_description(cur, tariff)
            except KeyError:
                True
            # data = [tariff['marketingId'], tariff['benefitsDescription']['description']]
            # cur.execute(f"INSERT INTO benefitsDescriptionDescr VALUES(?, ?)", data)
            #
            # insert_all_benefits_description_icons(cur, tariff)

            if data1[-2] == 0:  # configurable or ordinary
                insert_all_characteristics(cur, tariff)

                insert_all_product_features(cur, tariff)

                if data1[-3] == 0:  # ordinary
                    # data = [tariff['marketingId'], tariff['id']]
                    # cur.execute("INSERT INTO packages VALUES(?, ?)", data)
                    # print(tariff['subscriptionFee'])

                    insert_subscription_fee(cur, tariff, 'marketingId')

                else:  # configurable
                    insert_all_configurable_tariff_settings(cur, tariff)

                    insert_all_regulators_of_configurable_tariff_settings(cur, tariff)
            else:
                data = [tariff['marketingId'], tariff['parametrizedTariffSettings']['defaultPackagePrice']]
                cur.execute("INSERT INTO parametrizedTariffSettings VALUES(?, ?)", data)

                insert_formula_coefficients(cur, tariff)

                insert_all_parametrized_options_with_settings(cur, tariff)

                insert_all_option_options(cur, tariff)

        con.commit()


def extract_items(json_data):
    # extract_keys(json_data)
    tariffs = json_data['actualTariffs']
    # print(tariffs)
    i = 0
    print(len(tariffs))
    for tariff in tariffs:
        # if i <= 1:
        #     print(tariff)
        # elif i == 0:
        #     i += 1
        print(tariff, "\n")
        i += 1
        print(i)
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


def start():
    creation_of_db()
    parsed_json = parse()
    # print(parsed_json)
    extract_items(parsed_json)


if __name__ == "__main__":
    start()
