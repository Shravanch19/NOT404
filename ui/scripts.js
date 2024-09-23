eel.expose(Send_Quality_links);
eel.expose(Wait_Text)
eel.expose(Wait_Text_final)
eel.expose(Final_link)

let Series_name = "";
let Series_type = "";

function Wait_Text(data) {
    document.getElementById("Waiting-text").innerHTML = data;
}
function Wait_Text_final(data) {
    document.getElementById("Waiting-text-final").innerHTML = data;
}

function Final_link(data) {
    document.getElementById("Waiting-final").style.display = "none";
    document.getElementById("download-link-text").innerHTML = data
    document.getElementById("download-link").style.display = "flex";
}

function Send_Quality_links(data) {
    document.getElementById('Waiting').style.display = "none";
    const Quality_box = document.getElementById("Qualities");

    // Directly loop through the keys of the passed data
    for (const key in data) {
        const option = document.createElement("option");
        option.value = data[key]; // Assuming the key itself is the value you want
        option.text = key;
        Quality_box.appendChild(option);
    }

    document.getElementById('quality-selector').style.display = "flex";
}

document.getElementById('Quality-btn').addEventListener("click", function (event) {
    document.getElementById('input-box').style.display = "none";
    document.getElementById('Waiting-final').style.display = "flex";
    let Quality = document.getElementById('Qualities').value;
    eel.Download(Quality);
})

document.getElementById('download-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const isSeries = document.getElementById('is-series').checked;
    const is_Ind = document.getElementById('is-Ind').checked;
    const movieName = document.getElementById('movie-name').value;

    document.getElementById('download-form').style.display = "none";

    if (isSeries) {
        Series_name = movieName;
        Series_type = is_Ind;
        Seasons(movieName);
    }
    else {
        Quality_links()
        eel.Movie(movieName, is_Ind);
    }
});

document.getElementById('submit-btn').addEventListener("click", function (event) {
    const seasonNumber = document.getElementById('season-number').value;
    document.getElementById('select-container').style.display = "none";
    Quality_links()
    eel.Series(Series_name, Series_type, seasonNumber);
})

async function Seasons(name) {
    const seasons = document.getElementById('season-number');
    let omdb_api_key = 'a32d7c00'
    const OMDB = await fetch(`https://www.omdbapi.com/?apikey=${omdb_api_key}&t=${(name)}&type=series`);
    const data = await OMDB.json();
    const totalSeasons = data.totalSeasons;
    console.log(totalSeasons);

    for (let i = 1; i <= totalSeasons; i++) {
        let option = document.createElement("option");
        option.value = i;
        option.text = `Season ${i}`;
        seasons.appendChild(option);
        console.log("updated");
    }
    const season_select_container = document.getElementById('select-container');
    season_select_container.style.display = "flex";

}

function Quality_links() {
    document.getElementById("quality-links-container").style.display = "flex";
    document.getElementById("Waiting").style.display = "flex";

}
