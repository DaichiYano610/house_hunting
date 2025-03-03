async function searchData() {
    const address = document.getElementById("address").value.trim();
    const dist = document.getElementById("dist").value.trim();
    const resultsDiv = document.getElementById("results");

    if (!address) {
        alert("住所を入力してください");
        return;
    }

    resultsDiv.innerHTML = "<p>検索中...</p>";

    try {
        const response = await fetch(`http://127.0.0.1:8000/get_property/?address=${encodeURIComponent(address)}&dist=${encodeURIComponent(dist)}`);
        
        if (!response.ok) {
            throw new Error(`HTTPエラー: ${response.status}`);
        }

        const data = await response.json();

        resultsDiv.innerHTML = ""; // 結果をクリア

        if (!data.result_data || data.result_data.length === 0) {
            resultsDiv.innerHTML = "<p>該当する物件が見つかりませんでした。</p>";
            return;
        }

        const hit_num = document.createElement("div");
        hit_num.innerHTML = `<p>${data.num}件/${data.whole}件中</p>`;
        resultsDiv.appendChild(hit_num);

        data.result_data.forEach(item => {
            const card = document.createElement("div");
            card.className = "result-card";

            const buildingName = document.createElement("h3");
            buildingName.textContent = item.building.name;

            const buildingDetails = document.createElement("p");
            buildingDetails.innerHTML = `
                <strong>距離:</strong> ${item.distance}&nbsp;(km)&nbsp;&nbsp;※距離は前後します<br>
                <strong>カテゴリ:</strong> ${item.building.category}<br>
                <strong>住所:</strong> ${item.building.address}<br>
                <strong>築年数:</strong> ${item.building.age}<br>
                <strong>階数:</strong> ${item.building.floors}<br>
                <strong>駅:</strong> ${item.building.stations?.join("<br>") || "情報なし"}
            `;

            const roomInfoHeader = document.createElement("h4");
            roomInfoHeader.textContent = "部屋情報";

            card.appendChild(buildingName);
            card.appendChild(buildingDetails);
            card.appendChild(roomInfoHeader);

            item.rooms.forEach(room => {
                const roomDetails = document.createElement("div");
                roomDetails.innerHTML = `
                    <hr>
                    <p><strong>階:</strong> ${room.floor}</p>
                    <p><strong>家賃:</strong> ${room.rent} 円</p>
                    <p><strong>管理費:</strong> ${room.management_fee} 円</p>
                    <p><strong>敷金:</strong> ${room.deposit} ヶ月</p>
                    <p><strong>礼金:</strong> ${room.key_money} ヶ月</p>
                    <p><strong>間取り:</strong> ${room.layout}</p>
                    <p><strong>面積:</strong> ${room.size} m²</p>
                    <p><a href="${room.url}" target="_blank" rel="noopener noreferrer">詳細を見る</a></p>
                `;
                card.appendChild(roomDetails);
            });

            resultsDiv.appendChild(card);
        });
    } catch (error) {
        resultsDiv.innerHTML = `<p>エラーが発生しました: ${error.message}</p>`;
    }
}
