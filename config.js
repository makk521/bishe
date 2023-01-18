let config = {
    modules: [
      {
        module: "clock",
        position: "top_left",
      },
      {
        module: "compliments",
        position: "lower_third",
      },
      {
        module: "weather",
        position: "top_right",
        header: "Weather Forecast",
        config: {
            weatherProvider: "openweathermap",
            type: "forecast",
            location: "Shanghai",
            locationID: "1796236", //ID from http://bulk.openweathermap.org/sample/city.list.json.gz; unzip the gz file and find your city
            apiKey: "c6761080ac5a8fa1f1a4b88a526b0919"
        }
    },

    {
                module: "weather",
                position: "top_right",
                config: {
                weatherProvider: "openweathermap",
                type: "current",
                location: "Shanghai",
                locationID: "1796236", //ID from http://bulk.openweathermap.org/sample/city.list.json.gz; unzip the gz file and >       
            apiKey: "c6761080ac5a8fa1f1a4b88a526b0919",
            },
        },
    ],
  };
  


