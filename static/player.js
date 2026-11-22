const player = document.getElementById("video-player");
const status = document.getElementById("status");
const title = document.getElementById("movie-title");
const movieButtons = [...document.querySelectorAll(".movie[data-direct-url]")];
const search = document.getElementById("movie-search");
const count = document.getElementById("movie-count");
const noResults = document.getElementById("no-search-results");

movieButtons.forEach(button => {
    button.addEventListener("click", () => {
        movieButtons.forEach(item => item.removeAttribute("aria-current"));
        button.setAttribute("aria-current", "true");
        title.textContent = button.dataset.title;
        status.textContent = "Loading original video…";
        player.pause();
        player.src = button.dataset.directUrl;
        player.load();
        player.play().catch(() => {
            status.textContent = "Video ready. Press Play if playback did not start.";
        });
    });
});

player.addEventListener("playing", () => { status.textContent = "Playing original video"; });
player.addEventListener("waiting", () => {
    if (!player.paused) status.textContent = "Buffering video…";
});
player.addEventListener("error", () => {
    if (!player.error) return;
    const messages = {
        2: "The video could not be loaded from the server.",
        3: "Your browser could not decode this video format.",
        4: "This browser does not support the movie’s video or audio format."
    };
    status.textContent = messages[player.error.code] || "Video playback failed.";
});

search.addEventListener("input", () => {
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    movieButtons.forEach(button => {
        const matches = button.textContent.toLocaleLowerCase().includes(query);
        button.hidden = !matches;
        if (matches) visible++;
    });
    count.textContent = query
        ? `${visible} matching ${visible === 1 ? "movie" : "movies"}`
        : `${movieButtons.length} ${movieButtons.length === 1 ? "movie" : "movies"}`;
    noResults.hidden = visible !== 0 || movieButtons.length === 0;
});
