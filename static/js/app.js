
function App(){
    this.init = function(){
        $("#submit").on("click", this.submit_cb(this))
    }

    this.makeRequest = function(observer_details, sources){
        var baseUrl = window.location.hostname ;
        var requestUrl = baseUrl + "/get_ephem" ;
        console.log(observer_details)
        console.log(sources[0])
        var self = this;
        $.ajax({
            type: "POST",
            url:"/get_ephem",
            contentType:"application/json",
            data: JSON.stringify({observer_details:observer_details, sources:sources}),
            success: function(data){
                self.populateOutput.bind(self)(data.sources);
            },

        })
    }
    this.submit_cb = function(self){
        return function(){
            var lon = $("#lon").val()
            var lat = $("#lat").val()
            var el = $("#el").val()
            var ra = $("#ra").val()
            var dec = $("#dec").val();
            var name = $("#name").val();
            self.makeRequest({lat:lat,lon:lon,el:el},[{RAJ2000:ra,DECJ2000:dec,name:name}]);
        }
    }

    this.populateOutput = function(sources){
        $("#output").html(`
            <table class="u-full-width">
                <thead>
                <tr>
                    <th>Name</th>
                    <th>${sources[0].name}</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>RA</td>
                    <td>${sources[0].RA.toFixed(2)}</td>
                </tr>
                <tr>
                    <td>DEC</td>
                    <td>${sources[0].DEC.toFixed(2)}</td>
                </tr>
                <tr>
                    <td>Az</td>
                    <td>${sources[0].AZ.toFixed(2)}</td>
                </tr>
                <tr>
                    <td>Alt</td>
                    <td>${sources[0].ALT.toFixed(2)}</td>
                </tr>
                </tbody>
            </table>
        `)
    }


}

$(document).ready(function(){
    var app = new App();
    app.init();
})
