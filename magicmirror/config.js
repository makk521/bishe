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
        config: {
          weatherProvider: "openweathermap",
          type: "forecast",
          location: "Shanghai",
          locationID: "1796236", //ID from http://bulk.openweathermap.org/sample/city.list.json.gz; unzip the gz file and >        
          apiKey: "c6761080ac5a8fa1f1a4b88a526b0919",
          lang: "zh"
        },
      },
    //   {
    //     module: "weather",
    //     position: "top_right",
    //     config: {
    //         weatherProvider: "openweathermap",
    //         type: "current",
    //         location: "New York",
    //         locationID: "5128581", //ID from http://bulk.openweathermap.org/sample/city.list.json.gz; unzip the gz file and find your city
    //         apiKey: "YOUR_OPENWEATHER_API_KEY"
    //     }
    //   },
      {
        module: "calendar",
        position: "top_left", // This can be any of the regions. Best results in left or right regions.
        config: {
          // The config property is optional.
          // If no config is set, an example calendar is shown.
          // See 'Configuration options' for more information.
        },
      },
      {
        module: "helloworld",
        position: "bottom_bar", // This can be any of the regions.
        config: {
          // See 'Configuration options' for more information.
          text: "Hello world!",
        },
      },
    ],
  };
  