document.addEventListener("DOMContentLoaded", function () {
    const defaultScales = {
        "shop_distance": 500,
        "mall_distance": 2000,
        "hospital_distance": 1000,
        "school_distance": 3000,
        "kindergarten_distance": 1000,
        "park_distance": 500,
        "station_distance": 300,
        "police_distance": 1000,
        "sport_distance": 1000,
        "post_distance": 500,
        "railway_station_distance": 3000,
        "restaurant_distance": 1000,
        "entertainment_distance": 3000
    };

    const fields = [
        "shop", "mall", "hospital", "school", "kindergarten", "park", "station",
        "police", "sport", "post", "railway_station", "restaurant", "entertainment"
    ];

    fields.forEach(field => {
        const input = document.getElementById(`${field}_distance`);
        const checkbox = document.getElementById(`${field}_enabled`);

        const savedValue = localStorage.getItem(`${field}_distance`);
        const savedChecked = localStorage.getItem(`${field}_enabled`);

        if (input && checkbox) {
            input.value = savedValue !== null ? Number(savedValue) : defaultScales[`${field}_distance`];
            checkbox.checked = savedChecked !== null ? JSON.parse(savedChecked) : true;
        
            input.addEventListener("input", () => {
                localStorage.setItem(`${field}_distance`, input.value);
            });
        
            checkbox.addEventListener("change", () => {
                localStorage.setItem(`${field}_enabled`, checkbox.checked);
            });
        }        
    });

});





