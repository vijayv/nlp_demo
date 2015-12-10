var SingleTrackExplorer = React.createClass({
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
		return (
			<div>

				<div id="sidebar sidebar-button-container" className="col-xs-6 col-lg-2">
					<FilterButton id="plays" key="plays" sort_by={this.sortTracksBy}>plays</FilterButton>
					<FilterButton id="likes" key="likes" sort_by={this.sortTracksBy}>likes</FilterButton>
					<FilterButton id="reposts" key="reposts" sort_by={this.sortTracksBy}>reposts</FilterButton>
					<FilterButton id="comments" key="comments" sort_by={this.sortTracksBy}>comments</FilterButton>
					// TODO Implement Reset
				</div>

				<div className="col-xs-12 col-sm-6 col-lg-10">
					<SingleTrackData track_data={this.state.track_data} />
				</div>

			</div>
		);
	}
}); // End SingleTrackExplorer

var SingleTrackData = React.createClass({
	render: function() {
		return <ul>{this.createItems(this.props.track_data)}</ul>;},

		createItems: function(items) {
			var output = [];
			for (var i = 0; i < items.length; i++) {output.push(<li>{items[i]}</li>);
		} return output;
	}
}); // End SingleTrackData
