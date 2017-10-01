# Project 7: Later Flights Are Later (Data Viz)

## Summary

US Airlines are required to report their on-time performance, and this visualization exposes one key observation: flights scheduled to leave later in the day arrive (on average) later than flights scheduled in the morning.

This report incorporates a full year of flight data from August 2016 thru July 2017 (most recent 12 months available at time of writing); data is available from the [BTS](https://www.transtats.bts.gov/Tables.asp?DB_ID=120&DB_Name=Airline%20On-Time%20Performance%20Data&DB_Short_Name=On-Time).

<div class='tableauPlaceholder' id='viz1506483487414' style='position: relative'><noscript><a href='#'><img alt='On-Time Performance ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;On&#47;On-TimePerformance_1&#47;On-TimePerformance&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='2' /> <param name='site_root' value='' /><param name='name' value='On-TimePerformance_1&#47;On-TimePerformance' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;On&#47;On-TimePerformance_1&#47;On-TimePerformance&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1506483487414');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='1000px';vizElement.style.height='860px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>

[View on Tableau Public](https://public.tableau.com/views/On-TimePerformance_1/On-TimePerformance?:embed=y&:display_count=yes&publish=yes)

## Design
This Tableau story is a collection of three charts inspecting the relationship between number of flights, average delay, type of delay, time of day, and airline.

In the first chart, a simple bar graph easily shows the difference in number of flights and total average delay for each airline.

The second chart differentiates between types of delay over the course of the year. I originally used stacked bars here because I expected to find a difference between Summer and Winter, but found the more interesting story is that Late Aircraft are consistently the most common cause of delay.

The third chart looks at each airline and delay over hours of the day. Delay is a continuous variable: each flight reports delay versus schedule time down to the minute. In my visualization, I'm not looking at individual flights, so I aggregate delay with an average. Additionally, while this is a quantitative variable, the exact numeric value is of less interest than the change in that value as another variable (scheduled departure hour, airline) changes. For this reason, I chose to display delay along a color scale rather than on an axis. This choice was also made in order to allow for a more compact/simple view without needing to include a y-axis for each airline. 


## Feedback

See an earlier draft of this viz [on Tableau Public](https://public.tableau.com/profile/ercjns#!/vizhome/On-TimePerformance_1/On-TimePerformancev1).

1. *"The two keys on the second chart seem odd as they're keyed for the same thing?"*
I'm using color and shape to encode the same data (delay classification), but Tableau provides two separate legends. I agree that two legends is odd, but didn't see a way to fix this in Tableau. I'm only keeping the shape legend, as only color could cause issues for colorblind viewers.

2. *"I was studying sizes as much as color on the third chart, and that was a bit irrelevant."*
Using size and color for different values means it isn't super clear which is important. The viewer has a point that size is less important than color for getting my point across, so that's certainly something to think about. I updated the color scale (and its label) so the color should be easier to interpret.

3. *"I didn't understand the caption on the third chart until figuring out how the chart works"*
The last chart does have a lot of data to consume. I changed the captions so it should lead into the data and the takeaway a bit more clearly.

## Resources
* Udacity Course Materials
* Tableau Public Documentation
