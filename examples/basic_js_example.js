var sources = [{name: "ESO013-G012",
        RAJ2000: 0.29250263822381634 * (180./Math.pi),
        DECJ2000: -1.4016351371821572 * (180./Math.pi)}]

var observer_details = {lon:54.368591, lat:24.482149, el:0.0}

var payload = {observer_details:observer_details, sources:sources}

var success_cb = function(data){
    console.log(data.success)
}

$.ajax({
    type:"POST",
    contentType:"application/json",
    requestUrl:"/get_ephem",
    data: JSON.stringify(payload),
    success:success_cb
})
