window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        download_svg: function(n_clicks) {
            if (!n_clicks || typeof window.cy === "undefined") return window.dash_clientside.no_update;
            const svg = window.cy.svg({bg: "#ffffff"});
            const blob = new Blob([svg], {type: "image/svg+xml"});
            const a = document.createElement("a");
            a.href = URL.createObjectURL(blob);
            a.download = "graph.svg";
            a.click();
            return window.dash_clientside.no_update;
        }
    }
});
