var SongStats = require('./singletrack.js');
var Loader = require('halogen/ScaleLoader');
var TrackExplorer = React.createClass({

	getInitialState: function() {
		return {
			song_list: [],
			loading_icon: "show",
		}
	},

	componentDidMount: function() {
		this.sortTracksBy("plays");
	},

	updateStateData: function(update_url) {
		this.setState({
			loading_icon: "show",
		});

		$.ajax({
			url: update_url,
			dataType: 'json',
			cache: false,
			success: function(data) {
				this.setState({
					song_list: data,
					loading_icon: "hidden",
				});
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
			<div className="row">
				<div className="col-sm-2 col-md-2">
					<div className="btn-group-vertical" role="group" aria-label="...">
						<FilterButton id="plays" key="plays" sort_by={this.sortTracksBy}>Plays</FilterButton>
						<FilterButton id="likes" key="likes" sort_by={this.sortTracksBy}>Likes</FilterButton>
						<FilterButton id="reposts" key="reposts" sort_by={this.sortTracksBy}>Reposts</FilterButton>
						<FilterButton id="comments" key="comments" sort_by={this.sortTracksBy}>Comments</FilterButton>
					</div>
				</div>
				<div className="col-sm-10 col-md-10">
					<Loader
						className={this.state.loading_icon}
						color="#26A65B"
						size="16px"
						margin="4px"/>
					<SongList song_list={this.state.song_list} />
				</div>
			</div>
		);
	}
}); // End TrackExplorer

var FilterButton = React.createClass({
	clickfn: function() {
		var sort = this.props.id;
		this.props.sort_by(sort);
	},

	render: function() {
		return (
			<button
				id={this.props.id}
				className="btn btn-default"
				onClick={this.clickfn}
				type="button">
				{this.props.children}
			</button>
		)
	}
}); // End FilterButton

var SongList = React.createClass({
	render: function() {
		var songNodes = this.props.song_list.map(function(song) {
			return (
				<Song
					key={song.trackTitle}
					trackUsername={song.trackUsername}
					trackTitle={song.trackTitle}
					trackGenre={song.trackGenre}
					trackcurrentPlays={song.currentPlays}
					trackcurrentLikes={song.currentLikes}
					trackcurrentReposts={song.currentReposts}
					trackcurrentComments={song.currentComments}
					trackUrl={song.trackUrl}
					trackId={song.trackId} />
			)
		});

		return (
			<div>
				{songNodes}
			</div>
		);
	}
}); // End SongList

var Song = React.createClass({

	render: function() {
		return (
			<div className="row song">
				<div className="row">
					<div className="col-sm-12 col-md-12 col-lg-12">
						<h3>
							<a href={this.props.trackUrl}>{this.props.trackTitle} </a>
							<small>{this.props.trackUsername}</small>
						</h3>
						<p>{this.props.trackGenre}</p>
					</div>
				</div>
				<div className="row">
					<div className="col-sm-6 col-md-6 col-lg-6">
					</div>
					<div className="col-sm-6 col-md-6 col-lg-6">
						<p>{this.props.trackcurrentPlays}</p>
						<p>{this.props.trackcurrentLikes}</p>
						<p>{this.props.trackcurrentReposts}</p>
						<p>{this.props.trackcurrentComments}</p>
					</div>
				</div>
			</div>
		)
	}
}); // End Song

module.exports = TrackExplorer;
