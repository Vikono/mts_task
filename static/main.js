let form = document.getElementById('form');

function tariff_view(tariffs){
    const tariffList = document.getElementById("tariffs");
    for (const tariff of tariffs){
        // console.log(tariff);
        const tariffDiv =document.createElement("div");
        tariffDiv.className = "tariff";

        const tariffImage = document.createElement("div");
        tariffImage.className = "tariff-img";

        const img = document.createElement("img");
        img.src = tariff.cardImageUrl;
        img.width = 350;
        // console.log(img.src);
//        return img;
        tariffImage.appendChild(img);

        tariffDiv.appendChild(tariffImage);

        const tariffInfo =document.createElement("div");
        tariffInfo.className = "tariff-info";
        tariffInfo.innerHTML = `
            <h3>${tariff.title}</h3>
        `;
        if (tariff.description!=null){
            const tariffDescription = document.createElement("div");
            tariffDescription.innerHTML=`<p>${tariff.description}</p>`;
            tariffInfo.appendChild(tariffDescription);
        }
        if (tariff.benefitsDescription.description != null){
            const benefitsDescr = document.createElement("div");
            benefitsDescr.innerHTML = `<p>${tariff.benefitsDescription.description}</p>`
            const imgs = document.createElement("div");
            for (const img of tariff.benefitsDescription.icons){
                const benefitsIcon = document.createElement("img");
                benefitsIcon.src = img[0];
                // console.log(img[0]);
                benefitsIcon.width = 30;
                imgs.appendChild(benefitsIcon);
            }
            tariffInfo.appendChild(benefitsDescr);
            tariffInfo.appendChild(imgs);

        }

        if (tariff.tariffType == "HomeServicesTariff"){
            // console.log(tariff.tariffType);
            const totalPriceDiv = document.createElement("div");
            // console.log(tariff.HomeTariffs);
            for (const homeTariff of tariff.HomeTariffs){
                const PriceHTML = document.createElement("div");
                // console.log(homeTariff);
                if (homeTariff.connectionFee){
                    const connection = document.createElement("div");
                    connection.innerHTML = `<h6>Стоимость подключения: ${homeTariff.connectionFee.valueFormat} ${homeTariff.connectionFee.unit.display}</h6>`;
                    PriceHTML.appendChild(connection);
                }
                if (homeTariff.totalPrice.valueFormat != null){
                    // console.log(homeTariff.valueFormat);
                    const price = document.createElement("div");
                    price.innerHTML = `<h5>${homeTariff.totalPrice.valueFormat} ${homeTariff.totalPrice.unit.display}</h5>`;
                    PriceHTML.appendChild(price);
                }
                totalPriceDiv.appendChild(PriceHTML);

            }
            tariffInfo.appendChild(totalPriceDiv);


        }

        if (tariff.isConfigurable == 1){
            const packagesDiv = document.createElement("div");
            // console.log(tariff.marketingId);
            packagesDiv.innerHTML = `<h6>Возможные пакеты:<\h6>`
            for (const package of tariff.packages){
                const packageDiv = document.createElement("div");
                const subscripFeeTitle = package.subscriptionFee.title;
                const subscripFeeValue = package.subscriptionFee.value;
                const regOptionId = package.regulatorsOptionsIds[0];
                // console.log(subscripFeeTitle, subscripFeeValue, regOptionId);
                for (const regulator of tariff.regulators){
                    // console.log(regulator);
                    for (const option of regulator.options){
                        // console.log(option);
                        if (option.optionId == regOptionId){
                            // console.log(option);
                            packageDiv.innerHTML = `
                                <p>${option.label} - ${subscripFeeValue}</p>
                            `;
                            packagesDiv.appendChild(packageDiv);
                        }
                    }
                } 
            }
            tariffInfo.appendChild(packagesDiv);
        }

        // if (tariff.isConvergent == 1){

        // }

        const chars = tariff.characteristics;
        const tariffChars = document.createElement("div");
        tariffChars.className = "chars";
        if (chars[0] != null)
        {   const charsTitle = document.createElement("div");
            charsTitle.innerHTML = `<h5>Характеристики</h5>`;
            tariffChars.appendChild(charsTitle);
        }
        for (const characteristic of chars){
            const tariffChar = document.createElement("div");
            if (characteristic.baseParameter == "InternetPackage"){
                tariffChar.innerHTML = `<p>Пакет интернета: ${characteristic.value}</p>`;    
            }
            else if (characteristic.baseParameter == "MaxSpeed"){
                tariffChar.innerHTML = `<p>Скорость доступа: ${characteristic.value}</p>`;
            }
            else if (characteristic.baseParameter == "MinutesPackage"){
                tariffChar.innerHTML = `<p>Пакет минут: ${characteristic.value}</p>`;
            }
            else if (characteristic.baseParameter == "TvChannels"){
                tariffChar.innerHTML = `<p>Количество ТВ каналов: ${characteristic.value}</p>`;
            }
            else if (characteristic.baseParameter == "MessagesPackage") {
                tariffChar.innerHTML = `<p>Пакет минут: ${characteristic.value} ${characteristic.description}</p>`;
            }
            
            tariffChars.appendChild(tariffChar);
        }
        tariffInfo.appendChild(tariffChars);

        const subscriptionFee =tariff.subscriptionFee;
        if (subscriptionFee != null){
            const subscriptFee = document.createElement("div");
            if (subscriptionFee.value != null){
                subscriptFee.innerHTML = `<h5>${subscriptionFee.value}</h5>`;
                tariffInfo.appendChild(subscriptFee);}
            else if (subscriptionFee.numValue != null){
                // console.log(tariff.marketingId);
                // console.log(subscriptionFee.numValue, subscriptionFee.displayUnit);
                subscriptFee.innerHTML = `<h5>${subscriptionFee.numValue} ${subscriptionFee.displayUnit}</h5>`;
                tariffInfo.appendChild(subscriptFee);
            }
        }
        else if (tariff.defaultPackagePrice){
           
            
            const all_options = document.createElement("div");
            all_options.innerHTML = `<h6>Настраиваемые характеристики</h6>`;
            for (const option of tariff.parameterizedOptions){
                const optionDiv = document.createElement("div");
                const title = option.serviceType;
                const range_min = option.rangeSettings.minValue;
                const range_max = option.rangeSettings.maxValue;
                if (title == 'Sms'){
                    optionDiv.innerHTML = `<p>От ${range_min} до ${range_max} СМС</p>`;
                }
                else if (title == "Calls"){
                    optionDiv.innerHTML = `<p>От ${range_min} до ${range_max} минут</p>`;
                }
                else if (title == "Internet"){
                    optionDiv.innerHTML = `<p>От ${range_min} до ${range_max} Гб интернета</p>`;
                }
                
                all_options.appendChild(optionDiv);

            }
            tariffInfo.appendChild(all_options);

            const defaultPrice = document.createElement("div");
            defaultPrice.innerHTML = `<h5>${tariff.defaultPackagePrice[0]} ₽/мес (опции влияют на цену)</h5>`;
            tariffInfo.appendChild(defaultPrice);
        }

        

        tariffDiv.appendChild(tariffInfo);
        // tariffDiv.appendChild(tariffChars);

        tariffList.append(tariffDiv);

    }
}

function clearBox()
{
    document.getElementById('tariffs').innerHTML = "";
}

async function fetchTariffs(){
    const response = await fetch('http://localhost:8012/tariffs');
    // console.log(response)
    if (!response.ok){
        console.error("Error fetching tariffs:", response.status, response.statusText);
        return;}
    const tariffs = await response.json();
    console.log("Note! Not all information stored in database is present here");
    // console.log(tariffs)
    clearBox();
    tariff_view(tariffs);
}

async function event(){
    const response = await fetch('http://localhost:8012/tariffs/parce');
    if (!response.ok){
        console.error("Error fetching tariffs:", response.status, response.statusText);
        return;}

    const tariffs = await response.json();
    console.log("New information from mts tariffs is fetched from site");
    console.log("Note! Not all information stored in database is present here");
    clearBox();
    tariff_view(tariffs);

}

form.addEventListener("submit", (e) => {
    e.preventDefault();

    // let value = value1.value;
    event();
})

fetchTariffs();