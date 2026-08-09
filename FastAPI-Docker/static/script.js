const form = document.getElementById("prediction-form");
const button = document.getElementById("predict-button");

const resultSection = document.getElementById("result-section");
const scoreElement = document.getElementById("score");
const badgeElement = document.getElementById("quality-badge");
const progressElement = document.getElementById("quality-progress");
const interpretationElement =
    document.getElementById("interpretation-text");


const featureNames = [
    "fixed_acidity",
    "volatile_acidity",
    "citric_acid",
    "residual_sugar",
    "chlorides",
    "free_sulfur_dioxide",
    "total_sulfur_dioxide",
    "density",
    "ph",
    "sulphates",
    "alcohol"
];


form.addEventListener("submit", async function(event) {

    event.preventDefault();

    button.disabled = true;
    button.textContent = "Predicting...";


    try {

        const features = featureNames.map(function(name) {

            const value =
                document.getElementById(name).value;

            return Number(value);

        });


        const response = await fetch("/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                features: features
            })

        });


        if (!response.ok) {

            throw new Error(
                "Prediction request failed."
            );

        }


        const data = await response.json();

        const score = Number(data.predicted_quality);


        displayResult(score);


    } catch (error) {

        alert(
            "Unable to generate prediction. " +
            "Please check the inputs and try again."
        );

        console.error(error);

    } finally {

        button.disabled = false;
        button.textContent = "Predict Wine Quality";

    }

});


function displayResult(score) {

    resultSection.classList.remove("hidden");


    scoreElement.textContent =
        score.toFixed(2);


    progressElement.style.width =
        Math.min(Math.max(score / 10 * 100, 0), 100) + "%";


    let label;
    let explanation;


    if (score < 4) {

        label = "Low Quality";

        explanation =
            "The model estimates a relatively low " +
            "quality score. The physicochemical profile " +
            "is associated with wines that received lower " +
            "quality ratings in the training data.";

    }

    else if (score < 5) {

        label = "Below Average";

        explanation =
            "The predicted score is below the middle " +
            "of the quality scale. This suggests the " +
            "wine may have characteristics associated " +
            "with lower-rated wines in the dataset.";

    }

    else if (score < 6) {

        label = "Average";

        explanation =
            "The model estimates an average-quality wine. " +
            "Its measured characteristics are broadly " +
            "similar to wines receiving mid-range ratings " +
            "in the training dataset.";

    }

    else if (score < 7) {

        label = "Good";

        explanation =
            "The model estimates a good-quality wine. " +
            "Its physicochemical characteristics are " +
            "associated with wines that received above-" +
            "average quality ratings.";

    }

    else if (score < 8) {

        label = "Very Good";

        explanation =
            "The predicted score indicates a very good " +
            "wine. Its measured characteristics are " +
            "associated with higher-quality wines in " +
            "the dataset.";

    }

    else {

        label = "Excellent";

        explanation =
            "The model estimates an exceptionally high " +
            "quality score. The measured characteristics " +
            "are strongly associated with highly rated " +
            "wines in the dataset.";

    }


    badgeElement.textContent = label;

    interpretationElement.textContent =
        explanation;


    resultSection.scrollIntoView({
        behavior: "smooth"
    });

}
