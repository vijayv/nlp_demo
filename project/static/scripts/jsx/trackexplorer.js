var TrackExplorer = React.createClass({

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
			<div className="row">
				<div className="col-xs-6 col-lg-2">
					<div className="btn-group-vertical" role="group" aria-label="...">
						<FilterButton id="plays" key="plays" sort_by={this.sortTracksBy}>Plays</FilterButton>
						<FilterButton id="likes" key="likes" sort_by={this.sortTracksBy}>Likes</FilterButton>
						<FilterButton id="reposts" key="reposts" sort_by={this.sortTracksBy}>Reposts</FilterButton>
						<FilterButton id="comments" key="comments" sort_by={this.sortTracksBy}>Comments</FilterButton>
					</div>
				</div>
				<div className="col-xs-12 col-sm-6 col-lg-10">
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
			<table className="table table-striped">
				<thead>
					<tr>
						<th>Artist Name</th>
						<th>SongName</th>
						<th>Genre</th>
						<th>Plays</th>
						<th>Likes</th>
						<th>Reposts</th>
						<th>Comments</th>
					</tr>
				</thead>
				<tbody>
					{songNodes}
				</tbody>
			</table>
		);
	}
}); // End SongList

var Song = React.createClass({

	songClickfn: function() {
		// TODO Reimplement this in a more React oriented way
		console.log("songClickfn as")
	},

	render: function() {
		return (
			<tr>
				<td>
					<span
						className="glyphicon glyphicon-menu-right"
						aria-hidden="true"
						onClick={this.songClickfn}>
					</span>
					<a href={this.props.trackUrl}>{this.props.trackTitle}</a>
				</td>
				<td>{this.props.trackUsername}</td>
				<td>{this.props.trackGenre}</td>
				<td>{this.props.trackcurrentPlays}</td>
				<td>{this.props.trackcurrentLikes}</td>
				<td>{this.props.trackcurrentReposts}</td>
				<td>{this.props.trackcurrentComments}</td>
			</tr>
		)
	}
}); // End Song

module.exports = TrackExplorer;