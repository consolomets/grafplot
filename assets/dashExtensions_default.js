window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(event) {
            const cy = this;
            const png = cy.png({
                bg: "#ffffff"
            });
            const a = document.createElement("a");
            a.href = png;
            a.download = "graph.png";
            a.click();
        }

    }
});