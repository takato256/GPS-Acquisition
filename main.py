import streamlit as st
import streamlit.components.v1 as components

apiKey = st.secrets.apikey
authDomain = st.secrets.authdomain
databaseURL = st.secrets.databaseurl
projectId = st.secrets.projectid
storageBucket = st.secrets.storagebucket
messagingSenderId = st.secrets.messagingsenderid
appId = st.secrets.appid
measurementId = st.secrets.measurementid

components.html(
    f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GPS情報を取得</title>
        <script src="https://www.gstatic.com/firebasejs/4.1.3/firebase.js"></script>
    </head>
    <body>
        <main>
            <p id="gpsInfo">???</p>
            <button id="btnGpsCheck">GPS情報を取得する</button>
        </main>
        
        <script type="module">

        // FirebaseのSDK
        import {{ initializeApp }} from "https://www.gstatic.com/firebasejs/9.12.1/firebase-app.js";
        import {{ getAnalytics, setUserId }} from "https://www.gstatic.com/firebasejs/9.12.1/firebase-analytics.js";
        import {{ getDatabase, ref, child, get, onValue ,set}} from "https://www.gstatic.com/firebasejs/9.12.1/firebase-database.js";

        // Firebaseの初期設定
        const firebaseConfig = {{
            apiKey: "{apiKey}",
            authDomain: "{authDomain}",
            databaseURL: "{databaseURL}",
            projectId: "{projectId}",
            storageBucket: "{storageBucket}",
            messagingSenderId: "{messagingSenderId}",
            appId: "{appId}",
            measurementId: "{measurementId}"
        }};

        // Firebaseの初期化
        const app = initializeApp(firebaseConfig);
        const analytics = getAnalytics(app);
        const database = getDatabase(app);

        // データベースの情報を取得
        const db = getDatabase();


        // 表示箇所とGPSチェックボタン
        let gpsInfo, btnGpsCheck;
            
        // GPS用
        let WP;        // 位置情報取得識別ID
        let lat;    // 緯度
        let lon;    // 経度
    

        // 位置情報の取得に成功した場合（geolocation用関数）
        function SccCB(position){{
            // 緯度の取得
            lat = position.coords.latitude;
            // 経度の取得
            lon = position.coords.longitude;
            // 位置情報取得を終了
            stopWP();
            set(ref(db), {{
                //userLocation: lat + "," + lon
                userLocation: lat + "," + lon 
            }});
            // 緯度・経度表示
            alert("位置情報を更新しました");
            showGPS();
        }}
    
        
        // 位置情報の取得に失敗した場合（geolocation用関数）    
        function ErrCB(error){{
            alert("位置情報を取得できませんでした");
        }}
    
        
        // 位置情報の監視を停止（geolocation用関数）
        function stopWP(error){{
            navigator.geolocation.clearWatch(WP);
        }}
    
        
        // 位置情報を更新（geolocation用関数）
        function updateWP(error){{
            stopWP();
            // 端末の位置情報を継続的に取得する(navigator.geolocation.watchPosition)
            WP = navigator.geolocation.watchPosition(SccCB, ErrCB, {{enableHighAccuracy: true}});
        }}
    

        // GPS情報を整形して表示
        function showGPS(){{
            let value = "緯度は" + lat + "<br>";
            value += "経度は" + lon;
            gpsInfo.innerHTML = value;

        }}
    

        // 起動時の処理
        window.addEventListener("load", ()=>{{
            // DOM取得
            gpsInfo = document.getElementById("gpsInfo");
            btnGpsCheck = document.getElementById("btnGpsCheck");
            // GPSチェックボタンイベント
            btnGpsCheck.addEventListener("click", updateWP);

        }})
        </script>
    </body>
    </html> 
    """
)
