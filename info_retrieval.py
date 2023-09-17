import sqlite3


def get_tariff_characteristics(cursor, marketingid):
    cursor.execute("SELECT title, value, numValue, displayUnit, description, quotaUnit, \
                    isUnlimited, numValueType, baseParameter FROM characteristics WHERE marketingId = ?",
                   (marketingid,))
    keys = ['title', 'value', 'numValue', 'displayUnit', 'description', 'quotaUnit',
            'isUnlimited', 'numValueType', 'baseParameter']
    chars = cursor.fetchall()
    list_of_chars = []
    for i in chars:
        temp = dict(zip(keys, i))
        list_of_chars.append(temp)
    return list_of_chars


def get_product_labels(cursor, marketingid):
    cursor.execute("SELECT text, type, sortOrder FROM productLabels WHERE marketingId = ?", (marketingid,))
    labels = cursor.fetchall()
    keys = ['text', 'type', 'sortOrder']
    list_of_labels = []
    for i in labels:
        temp = dict(zip(keys, i))
        list_of_labels.append(temp)
    return list_of_labels


def get_product_features(cursor, marketingid):
    cursor.execute("SELECT title, value, isUnlimited, numValueType, iconUrl, baseParameter \
                    FROM productFeatures WHERE marketingId = ?", (marketingid,))
    features = cursor.fetchall()
    keys = ['title', 'value', 'isUnlimited', 'numValueType', 'iconUrl', 'baseParameter']
    list_of_features = []
    for i in features:
        temp = dict(zip(keys, i))
        list_of_features.append(temp)
    return list_of_features


def get_benefits_descr(cursor, marketingid):
    cursor.execute("SELECT descr FROM benefitsDescriptionDescr WHERE marketingId = ?", (marketingid,))
    descr = cursor.fetchone()
    cursor.execute("SELECT icon FROM benefitsDescriptionIcons WHERE marketingId = ?", (marketingid,))
    icons = cursor.fetchall()
    return dict(zip(['description', 'icons'], [descr, icons]))


def get_subscription_fee(cursor, id):
    cursor.execute("SELECT title, value, numValue, displayUnit, quotaUnit, quotaPeriod, \
            isUnlimited, numValueType, sortOrder, baseParameter FROM subscriptionFee WHERE id = ?", (id,))
    subscription_fee = cursor.fetchone()
    # print(subscription_fee)
    keys = ['title', 'value', 'numValue', 'displayUnit', 'quotaUnit', 'quotaPeriod',
            'isUnlimited', 'numValueType', 'sortOrder', 'baseParameter']
    try:
        fee = dict(zip(keys, subscription_fee))
        return fee
    except TypeError:
        return subscription_fee


def get_tariff_package_ids(cursor, marketingid):
    cursor.execute("SELECT id FROM packages WHERE marketingId=?", (marketingid,))
    ids = cursor.fetchall()
    return ids


def get_tariff_packages(cursor, marketingid):
    ids = get_tariff_package_ids(cursor, marketingid)
    list_of_packages = []
    for i in ids:
        # print(i)
        cursor.execute("SELECT regulatorsOptionsId FROM regulatorsOpIds WHERE id = ?", i)
        regulatorIds = cursor.fetchall()
        # print(regulatorIds)
        reg_ids = []
        for j in regulatorIds:
            reg_ids.append(j[0])
        # all_regs.add(i[0] for i in regulatorIds)
        subscrip_fee = get_subscription_fee(cursor, i[0])
        keys = ['id', 'subscriptionFee', 'regulatorsOptionsIds']
        temp = dict(zip(keys, [i[0], subscrip_fee, reg_ids]))
        list_of_packages.append(temp)
    # print(all_regs)
    return list_of_packages


def get_tariff_regulators(cursor, marketingid):
    # print(marketingid)
    cursor.execute("SELECT regulatorsOptionsId, sortOrder, quotaType FROM regulators WHERE marketingId = ?",
                   (marketingid,))

    keys = ['id', 'sortOrder', 'quotaType']
    regs_info = cursor.fetchall()
    regs = []
    for i in regs_info:
        reg = dict(zip(keys, i))
        reg['options'] = get_regulator_options(cursor, i[0])
        regs.append(reg)

    # print(reg_info)
    return regs


def get_regulator_oprions_ids(cursor, reg_id):
    cursor.execute("SELECT optionId FROM regOptionsId WHERE regulatorsOptionsId=?", (reg_id,))
    return cursor.fetchall()


def get_option_quotas(cursor, option_id):
    cursor.execute("SELECT title, value, displayUnit, quotaUnit, \
                isUnlimited, numValueType, sortOrder, baseParameter FROM opIdQuotas WHERE optionId =?", option_id)
    quotas = cursor.fetchall()
    keys = ['title', 'value', 'displayUnit', 'quotaUnit',
            'isUnlimited', 'numValueType', 'sortOrder', 'baseParameter']
    list_of_quotas = []
    for op in quotas:
        temp = dict(zip(keys, op))
        list_of_quotas.append(temp)
    return list_of_quotas


def get_option(cursor, option_id):
    # print(option_id)
    cursor.execute("SELECT optionId, label, valTitle, valValue, \
                valNumValue, valDisplayUnit, valIsUnlimited, valNumValueType, \
                valSortOrder, valBaseParameter FROM options WHERE optionId=?", option_id)
    option = cursor.fetchone()
    keys = ['optionId', 'label']
    op = dict(zip(keys, option[:2]))
    keys = ["title", "value", "numValue", "displayUnit", "quotaUnit",
            "isUnlimited", "numValueType", "sortOrder", "baseParameter"]
    op['value'] = dict(zip(keys, option[2:]))
    op['quotas'] = get_option_quotas(cursor, option_id)
    return op


def get_regulator_options(cursor, reg_id):
    options_ids = get_regulator_oprions_ids(cursor, reg_id)
    keys = ['optionId', 'label', 'valTitle', 'valValue',
            'valNumValue', 'valDisplayUnit', 'valIsUnlimited', 'valNumValueType',
            'valSortOrder', 'valBaseParameter']
    options = []
    for op_id in options_ids:
        temp = get_option(cursor, op_id)
        options.append(temp)
    return options


# def get_tariff_package_regulators(cursor, marketingid):
#     regs = []
#     for reg_id in regs_ids:
#         print(reg_id)
#         reg = get_regulator_info(cursor, reg_id)
#         regs.append(reg)
#     return regs
def get_tariff_total_price(cursor, tariffid):
    cursor.execute("SELECT valueFormat, value, unitDisplay, unitPeriodDisplay, \
            unitPeriodMultiplier, uUnitDisplay, unitQuotaPeriod FROM totalPrice WHERE tariffId = ?", (tariffid,))
    totalprix = cursor.fetchone()
    keys = ['valueFormat', 'value']
    price = dict(zip(keys, totalprix[:2]))
    keys = ["display",
            "periodDisplay",
            "periodMultiplier",
            "unitDisplay",
            "quotaPeriod"]
    price['unit'] = dict(zip(keys, totalprix[2:]))
    return price


def get_connection_fee(cursor, tariffid):
    cursor.execute("SELECT valueFormat, value, unitDisplay, \
                unitPeriodDisplay, unitPeriodMultiplier, \
                uUnitDisplay, unitQuotaPeriod FROM connectionFee WHERE id = ?", (tariffid,))
    con_fee = cursor.fetchone()
    keys = ['valueFormat', 'value']
    fee = dict(zip(keys, con_fee[:2]))
    keys = ["display",
            "periodDisplay",
            "periodMultiplier",
            "unitDisplay",
            "quotaPeriod"]
    fee['unit'] = dict(zip(keys, con_fee[2:]))
    return fee


def get_tariff_family(cursor, tariffid):
    cursor.execute("SELECT id, title, alias, hasFamilyCard FROM family WHERE tariffId = ?", (tariffid,))
    family = cursor.fetchone()
    keys = ['id', 'title', 'alias', 'hasFamilyCard']
    return dict(zip(keys, family))


def get_home_tariffs(cursor, marketingid):
    cursor.execute("SELECT id, title, description, alias, htorder, phoneTariff, \
                bigListImageHero1, bigListImageHero2, cardImageUrl FROM homeTariffs WHERE marketingId = ?",
                   (marketingid,))
    tariffs = cursor.fetchall()
    all_home_tariffs = []
    keys = ['id', 'title', 'description', 'alias', 'order', 'phoneTariffId',
            'bigListImageHero1', 'bigListImageHero2', 'cardImageUrl']
    for tariff in tariffs:
        temp = dict(zip(keys, tariff))
        temp['totalPrice'] = get_tariff_total_price(cursor, tariff[0])
        try:
            temp['connectionFee'] = get_connection_fee(cursor, tariff[0])
        except TypeError:
            True
        temp['family'] = get_tariff_family(cursor, tariff[0])
        all_home_tariffs.append(temp)
    return all_home_tariffs


def get_pv_package(cursor, marketingid):
    cursor.execute("SELECT id, alias, isSatellite, isIpTv, isIpTv2, isDvbc, isBase, titleForSite, channelsHdCount, \
            channelsUhdCount, channelsCount, forDTV, forInteractiveTv, external FROM tvPackage WHERE marketingId = ?",
                   (marketingid,))
    tv_package = cursor.fetchone()
    keys = ['id', 'alias', 'isSatellite', 'isIpTv', 'isIpTv2', 'isDvbc', 'isBase', 'titleForSite', 'channelsHdCount',
            'channelsUhdCount', 'channelsCount', 'forDTV', 'forInteractiveTv', 'external']
    try:
        tv = dict(zip(keys, tv_package))
    except TypeError:
        return None
    return tv


def get_rent_price(cursor, rentid):
    cursor.execute("SELECT valueFormat, value, \
                    unitDisplay, unitPeriodDisplay, unitPeriodMultiplier, \
                    uUnitDisplay, unitQuotaPeriod FROM rentPrice WHERE id = ?", (rentid,))
    rent_price = cursor.fetchone()
    keys = ['valueFormat', 'value']
    rent = dict(zip(keys, rent_price[:2]))
    keys = ["display",
            "periodDisplay",
            "periodMultiplier",
            "unitDisplay",
            "quotaPeriod"]
    rent['unit'] = dict(zip(keys, rent_price[2:]))
    return rent


def get_sale_price(cursor, saleid):
    cursor.execute("SELECT valueFormat, value, \
                        unitDisplay, unitPeriodDisplay, unitPeriodMultiplier, \
                        uUnitDisplay, unitQuotaPeriod FROM salePrice WHERE id = ?", (saleid,))
    sale_price = cursor.fetchone()
    keys = ['valueFormat', 'value']
    try:
        sale = dict(zip(keys, sale_price[:2]))
        keys = ["display",
                "periodDisplay",
                "periodMultiplier",
                "unitDisplay",
                "quotaPeriod"]
        sale['unit'] = dict(zip(keys, sale_price[2:]))
    except TypeError:
        return None
    return sale


def get_devices(cursor, marketingid):
    cursor.execute("SELECT deviceId FROM tariffDevices WHERE marketingId = ?", (marketingid,))
    devices_ids = cursor.fetchall()
    all_devices = []
    for dev_id in devices_ids:
        cursor.execute("SELECT archive, forInteractiveTv, isInternet, isMandatory, isOverrideRentPrice, isPhone, isTv, \
                isCctv, rentUnavailable, saleUnavailable, title, sortOrder, rentPriceId, salePriceId FROM devices WHERE id = ?",
                       dev_id)
        keys = ['archive', 'forInteractiveTv', 'isInternet', 'isMandatory', 'isOverrideRentPrice', 'isPhone', 'isTv',
                'isCctv', 'rentUnavailable', 'saleUnavailable', 'title', 'sortOrder']
        dev_info = cursor.fetchone()
        device = dict(zip(keys, dev_info[-2:]))

        device['rentPrice'] = get_rent_price(cursor, dev_info[-2])
        device['salePrice'] = get_sale_price(cursor, dev_info[-1])
        all_devices.append(device)

    return all_devices


def get_all_tariff_actions(cursor, marketingid):
    cursor.execute("SELECT actionId FROM tariffActions WHERE marketingId = ?", (marketingid,))
    actions = cursor.fetchall()
    all_actions = []
    for action_id in actions:
        cursor.execute("SELECT title, promoPeriod, isArchive, discountAbsolute, isDefault, \
            isHidden, highlightAfterPromo, isApplied FROM actions WHERE id = ?", action_id)
        action = cursor.fetchone()
        keys = ['title', 'promoPeriod', 'isArchive', 'discountAbsolute', 'isDefault',
                'isHidden', 'hihglightAfterPromo', 'isApplied']
        temp = dict(zip(keys, action))
        all_actions.append(temp)
    return all_actions


def get_default_package_price(cursor, marketingid):
    cursor.execute("SELECT defaultPrice FROM parametrizedTariffSettings WHERE marketingId = ?", (marketingid,))
    price = cursor.fetchone()
    return price


def get_formula_coeffs(cursor, marketingid):
    cursor.execute("SELECT useForMinutesPackage, regional, useForInternetPackage, \
            useForMessagesPackage, additional FROM coeffs WHERE marketingId = ?", (marketingid,))
    keys = ['useForMinutesPackage', 'regional', 'useForInternetPackage',
            'useForMessagesPackage', 'additional']
    coeffs = dict(zip(keys, cursor.fetchone()))
    return coeffs


def get_parameterized_options(cursor, marketinid):
    cursor.execute("SELECT id, serviceType, sortOrder FROM parametrizedOptions WHERE marketingId = ?", (marketinid,))
    options = cursor.fetchall()
    all_options = []
    for op in options:
        cursor.execute("SELECT defaultValue, defaultValueForAuthorized, minValue, maxValue, step, isValid FROM \
                        rangeSettings WHERE paramOpId = ?", (op[0],))
        range_set = cursor.fetchone()
        keys = ['id', 'serviceType', 'sortOrder']
        option = dict(zip(keys, op))
        keys = ['defaultValue', 'defaultValueForAuthorized', 'minValue', 'maxValue', 'step', 'isValud']
        option['rangeSettings'] = dict(zip(keys, range_set))
        all_options.append(option)
    return all_options


def get_tariff_options(cursor, marketingid):
    cursor.execute("SELECT id, title, isDefault FROM parametrizedOptionOptions WHERE marketingId=?", (marketingid,))
    keys = ['id', 'title', 'isDefault']
    options = cursor.fetchall()
    all_options = []
    for op in options:
        temp = dict(zip(keys, op))
        all_options.append(temp)
    return all_options


def get_tariff_parameters(tariff):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        marketingid = tariff['marketingId']
        tariff['characteristics'] = get_tariff_characteristics(cur, marketingid)
        tariff['productLabels'] = get_product_labels(cur, marketingid)
        tariff['productFeatures'] = get_product_features(cur, marketingid)
        tariff['benefitsDescription'] = get_benefits_descr(cur, marketingid)
        if tariff['isConfigurable'] == 1:
            tariff['packages'] = get_tariff_packages(cur, marketingid)
            # print(regsId)
            tariff['regulators'] = get_tariff_regulators(cur, marketingid)
        elif tariff['tariffType'] == 'HomeServicesTariff':
            tariff['HomeTariffs'] = get_home_tariffs(cur, marketingid)
        elif tariff['isConvergent'] == 1:
            tariff['subscriptionFee'] = get_subscription_fee(cur, marketingid)
            tariff['tvPackage'] = get_pv_package(cur, marketingid)
            tariff['devices'] = get_devices(cur, marketingid)
            tariff['actions'] = get_all_tariff_actions(cur, marketingid)
        elif tariff['isParametrized'] == 1:
            tariff['defaultPackagePrice'] = get_default_package_price(cur, marketingid)
            tariff['formulaCoefficients'] = get_formula_coeffs(cur, marketingid)
            tariff['parameterizedOptions'] = get_parameterized_options(cur, marketingid)
            tariff['options'] = get_tariff_options(cur, marketingid)
        else:
            tariff['subscriptionFee'] = get_subscription_fee(cur, marketingid)

        return tariff


def get_all_tariffs():
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM info")
        tariffs = cur.fetchall()
        keys = ['marketingId', 'id', 'alias', 'title', 'description',
                'cardImageUrl', 'priority', 'isPriorityProduct', 'tariffType',
                'isConfigurable', 'isParametrized', 'isConvergent']
        i = 0
        all_tariffs = []
        for each in tariffs:
            tariff_data = dict(zip(keys, each))
            print(tariff_data['marketingId'])
            t_and_ch = get_tariff_parameters(tariff_data)
            all_tariffs.append(t_and_ch)
            i += 1
            print(i, "\n", t_and_ch, "\n")
        print(i)
        return all_tariffs

# get_all_tariffs()
