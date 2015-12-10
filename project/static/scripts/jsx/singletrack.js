var LineChart = require("react-chartjs").Line;

var SongStats = React.createClass({
	getInitialState: function() {
		return {
			track_data: {dailyPlays: []},
		}
	},

	componentWillMount: function() {
		this.getTrackData(this.props.trackId);
	},

	getTrackData: function(val) {
		var base_uri = "/api/v1/track?track_id=";
		var trackId = val;
		var formattedUrl = base_uri + trackId;
		this.updateStateData(formattedUrl);
		return formattedUrl;
	},

	updateStateData: function(update_url) {
		$.ajax({
			url: update_url,
			dataType: 'json',
			cache: false,
			success: function(data) {
				this.setState({track_data: data.dailyAggregatePlays});
			}.bind(this),
			error: function(xhr, status, err) {
				console.error("/api/v1/track", status, err.toString());
			}.bind(this)
		});
	},

	render: function() {
		var chart_data = {datasets: [{data: this.state.track_data}]}
		var chart_options = {}
		return (
			<LineChart data={chart_data} options={chart_options} width="600" height="250"/>
		);
	}
}); // End SingleTrackExplorer


module.exports = SongStats;
