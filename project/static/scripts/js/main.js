(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);throw new Error("Cannot find module '"+o+"'")}var f=n[o]={exports:{}};t[o][0].call(f.exports,function(e){var n=t[o][1][e];return s(n?n:e)},f,f.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
var TrackExplorer = require('./trackexplorer.js');

var SingleTrackExplorer = React.createClass({displayName: "SingleTrackExplorer",
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
			React.createElement("div", null, 

				React.createElement("div", {id: "sidebar sidebar-button-container", className: "col-xs-6 col-lg-2"}, 
					React.createElement(FilterButton, {id: "plays", key: "plays", sort_by: this.sortTracksBy}, "plays"), 
					React.createElement(FilterButton, {id: "likes", key: "likes", sort_by: this.sortTracksBy}, "likes"), 
					React.createElement(FilterButton, {id: "reposts", key: "reposts", sort_by: this.sortTracksBy}, "reposts"), 
					React.createElement(FilterButton, {id: "comments", key: "comments", sort_by: this.sortTracksBy}, "comments"), 
					"// TODO Implement Reset"
				), 

				React.createElement("div", {className: "col-xs-12 col-sm-6 col-lg-10"}, 
					React.createElement(SingleTrackData, {track_data: this.state.track_data})
				)

			)
		);
	}
}); // End SingleTrackExplorer

var SingleTrackData = React.createClass({displayName: "SingleTrackData",
	render: function() {
		return React.createElement("ul", null, this.createItems(this.props.track_data));},

		createItems: function(items) {
			var output = [];
			for (var i = 0; i < items.length; i++) {output.push(React.createElement("li", null, items[i]));
		} return output;
	}
}); // End SingleTrackData

React.render(
	React.createElement(TrackExplorer, null),
	document.getElementById('content')
);


},{"./trackexplorer.js":2}],2:[function(require,module,exports){
var TrackExplorer = React.createClass({displayName: "TrackExplorer",

	getInitialState: function() {
		return {
			song_list: [],
		}
	},

	componentDidMount: function() {
		this.sortTracksBy("plays");
	},

	updateStateData: function(update_url) {
		$.ajax({
			url: update_url,
			dataType: 'json',
			cache: false,
			success: function(data) {
				this.setState({song_list: data});
			}.bind(this),
			error: function(xhr, status, err) {
				console.error("/api/v1/tracks", status, err.toString());
			}.bind(this)
		});
	},

	sortTracksBy: function(val) {
		var base_uri = "/api/v1/tracks?fields=track_id;track_user_name;track_title;track_genre;current_plays;current_likes;current_reposts;current_comments;track_url&limit=100&sort="
		switch (val) {
			case "plays":
				this.updateStateData(base_uri + "current_plays");
				break;
			case "likes":
				this.updateStateData(base_uri + "current_likes");
				break;
			case "reposts":
				this.updateStateData(base_uri + "current_reposts");
				break;
			case "comments":
				this.updateStateData(base_uri + "current_comments");
				break;
			default:
				this.updateStateData(base_uri + "current_likes");
				break;
		}
	},

	render: function() {
		return (
			React.createElement("div", {className: "row"}, 
				React.createElement("div", {className: "col-xs-6 col-lg-2"}, 
					React.createElement("div", {className: "btn-group-vertical", role: "group", "aria-label": "..."}, 
						React.createElement(FilterButton, {id: "plays", key: "plays", sort_by: this.sortTracksBy}, "Plays"), 
						React.createElement(FilterButton, {id: "likes", key: "likes", sort_by: this.sortTracksBy}, "Likes"), 
						React.createElement(FilterButton, {id: "reposts", key: "reposts", sort_by: this.sortTracksBy}, "Reposts"), 
						React.createElement(FilterButton, {id: "comments", key: "comments", sort_by: this.sortTracksBy}, "Comments")
					)
				), 
				React.createElement("div", {className: "col-xs-12 col-sm-6 col-lg-10"}, 
					React.createElement(SongList, {song_list: this.state.song_list})
				)
			)
		);
	}
}); // End TrackExplorer

var FilterButton = React.createClass({displayName: "FilterButton",
	clickfn: function() {
		var sort = this.props.id;
		this.props.sort_by(sort);
	},

	render: function() {
		return (
			React.createElement("button", {
				id: this.props.id, 
				className: "btn btn-default", 
				onClick: this.clickfn, 
				type: "button"}, 
				this.props.children
			)
		)
	}
}); // End FilterButton

var SongList = React.createClass({displayName: "SongList",
	render: function() {
		var songNodes = this.props.song_list.map(function(song) {
			return (
				React.createElement(Song, {
					key: song.trackTitle, 
					trackUsername: song.trackUsername, 
					trackTitle: song.trackTitle, 
					trackGenre: song.trackGenre, 
					trackcurrentPlays: song.currentPlays, 
					trackcurrentLikes: song.currentLikes, 
					trackcurrentReposts: song.currentReposts, 
					trackcurrentComments: song.currentComments, 
					trackUrl: song.trackUrl, 
					trackId: song.trackId})
			)
		});

		return (
			React.createElement("table", {className: "table table-striped"}, 
				React.createElement("thead", null, 
					React.createElement("tr", null, 
						React.createElement("th", null, "Artist Name"), 
						React.createElement("th", null, "SongName"), 
						React.createElement("th", null, "Genre"), 
						React.createElement("th", null, "Plays"), 
						React.createElement("th", null, "Likes"), 
						React.createElement("th", null, "Reposts"), 
						React.createElement("th", null, "Comments")
					)
				), 
				React.createElement("tbody", null, 
					songNodes
				)
			)
		);
	}
}); // End SongList

module.exports = TrackExplorer;


},{}]},{},[1])