document.addEventListener("DOMContentLoaded", async () => {

    const website = document.getElementById("website");
    const score = document.getElementById("score");
    const rating = document.getElementById("rating");
    const grade = document.getElementById("grade");

    const badges = document.getElementById("badges");
    const tips = document.getElementById("tips");

    const progress = document.getElementById("progress");

    const radius = 50;
    const circumference = 2 * Math.PI * radius;

    progress.style.strokeDasharray = circumference;
    progress.style.strokeDashoffset = circumference;


    try {

        const [tab] = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });


        if (!tab || !tab.url) {

            throw new Error("Unable to detect current website.");

        }


        website.textContent = tab.url;


        if (
            tab.url.startsWith("chrome://") ||
            tab.url.startsWith("edge://") ||
            tab.url.startsWith("about:")
        ) {

            score.textContent = "--";

            rating.textContent = "Browser Page";

            grade.textContent = "";

            badges.innerHTML =
                '<div class="badge warn">Cannot Scan Browser Pages</div>';

            tips.innerHTML =
                "<li>Open a normal website first.</li>";

            return;

        }



        const response = await fetch(
            "http://127.0.0.1:5000/scan",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    url: tab.url
                })

            }
        );


        if (!response.ok) {

            throw new Error(
                "Server returned status " + response.status
            );

        }


        const data = await response.json();


        console.log("Scanner response:", data);



        if (!data.success) {

            throw new Error(
                "Scanner failed to analyze website."
            );

        }



        const scanScore = Number(data.score) || 0;


        score.textContent = scanScore;



        const offset =
            circumference -
            (scanScore / 100) * circumference;


        progress.style.strokeDashoffset = offset;



        badges.innerHTML = "";
        tips.innerHTML = "";



        // Score Rating

        if (scanScore >= 80) {

            progress.style.stroke = "#22C55E";

            rating.textContent =
                "Excellent Privacy";

        }

        else if (scanScore >= 60) {

            progress.style.stroke = "#FACC15";

            rating.textContent =
                "Moderate Privacy";

        }

        else {

            progress.style.stroke = "#EF4444";

            rating.textContent =
                "High Privacy Risk";

        }



        grade.textContent =
            "Grade " + (data.grade || "N/A");




        function badge(text, type) {

            const div =
                document.createElement("div");

            div.className =
                "badge " + type;

            div.textContent = text;

            badges.appendChild(div);

        }




        const risks =
            Array.isArray(data.risks)
                ? data.risks
                : [];



        const suggestions =
            Array.isArray(data.suggestions)
                ? data.suggestions
                : [];



        // HTTPS

        if (data.url && data.url.startsWith("https://")) {

            badge("HTTPS", "good");

        }

        else {

            badge("HTTP", "bad");

        }



        // Privacy Policy

        if (
            risks.some(
                r => r.includes("Privacy Policy")
            )
        ) {

            badge(
                "No Privacy Policy",
                "bad"
            );

        }

        else {

            badge(
                "Privacy Policy",
                "good"
            );

        }




        // Trackers

        const trackerChecks = [

            ["Cookies", "Cookies", "warn"],

            ["Google Analytics", "Google Analytics", "warn"],

            ["Google Tag Manager", "Tag Manager", "warn"],

            ["Facebook", "Facebook Pixel", "bad"],

            ["Hotjar", "Hotjar", "warn"],

            ["Mixpanel", "Mixpanel", "warn"],

            ["Clarity", "Microsoft Clarity", "warn"]

        ];



        trackerChecks.forEach(item => {

            if (
                risks.some(
                    r => r.includes(item[0])
                )
            ) {

                badge(
                    item[1],
                    item[2]
                );

            }

        });




        if (suggestions.length > 0) {


            suggestions.forEach(tip => {

                const li =
                    document.createElement("li");

                li.textContent = tip;

                tips.appendChild(li);

            });


        }

        else {

            tips.innerHTML =
                "<li>No suggestions.</li>";

        }



    }


    catch (err) {


        console.error(
            "Privacy Scanner Error:",
            err
        );


        score.textContent = "--";

        rating.textContent =
            "Scan Error";

        grade.textContent =
            "";


        progress.style.stroke =
            "#9CA3AF";


        badges.innerHTML =
            `<div class="badge bad">
                ${err.message}
            </div>`;


        tips.innerHTML =
            "<li>Check Flask backend and extension permissions.</li>";

    }


});