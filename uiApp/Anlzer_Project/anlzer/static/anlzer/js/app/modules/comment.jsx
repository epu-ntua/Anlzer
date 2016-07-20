/**
 * Created by DarkA_000 on 5/9/2016.
 */

var project = window.location.href.split('/projects/')[1].split('/')[0];

var CommentList = React.createClass({
  render: function() {
    var commentNodes = this.props.data.map(function(comment) {
      return (
        <Comment author={comment.author} key={comment.id} date={comment.date}>
          {comment.text}
        </Comment>
      );
    });
    return (
      <div className="comment-list col-xs-12">
        {commentNodes}
      </div>
    );
  }
});

// Outer Comment Box
var Comment = React.createClass({
  render: function() {
    return (
      <div className="comment col-xs-12">
        <div className="comment-date pull-right">{this.props.date}</div>
        <div className="comment-author pull-left">{this.props.author}</div>
        <div className="comment-text col-xs-12">{this.props.children}</div>
      </div>
    );
  }
});

var CommentForm = React.createClass({

  getInitialState: function() {
    return { text: ''};
  },

  handleTextChange: function(e) {
    this.setState({text: e.target.value});
  },

  handleSubmit: function(e) {
      e.preventDefault();

      if (!this.state.text) return;
        console.log(this.state.text.trim())
      $.ajax({
          url: this.props.url,
          type: 'POST',
          dataType: 'text',
          data: {
              'csrfmiddlewaretoken': getCookie('csrftoken'),
              'message': this.state.text.trim()
          },

          success: function() {
            // Update the data's state
            this.setState({text: ''});
            this.props.onCommentSubmit()

          }.bind(this),

          error: function(xhr, status, err) {

              console.error('An Error occured');
          }.bind(this)
      });
  },

  render: function() {
    return (
      <form className="comment-form col-xs-12 anlzer-form" onSubmit={this.handleSubmit}>
        <input className="input-lg col-xs-12 no-highlight" type="text" value={this.state.text} onChange={this.handleTextChange} placeholder="Type your comment..." />
        <button type="submit" className="btn anlzer-btn col-xs-4 no-highlight" style={{'marginLeft':0, 'marginTop': '15px'}} value="Post">Post</button>
      </form>
    );
  }
});

// Outer Comment Box
var CommentBox = React.createClass({
  getInitialState: function() {
    return {data: []};
  },
  loadCommentsFromServer: function() {
      $.ajax({
          url: this.props.url,
          type: 'GET',
          dataType: 'json',
          // data: {'csrfmiddlewaretoken': getCookie('csrftoken')},

          success: function(data) {
            // Update the data's state
            this.setState({data: data});


          }.bind(this),

          error: function(xhr, status, err) {

              console.error('An Error occured');
          }.bind(this)
      });

    var $commentList = $(ReactDOM.findDOMNode(this.refs.CommentList));
    $commentList.perfectScrollbar('destroy').perfectScrollbar()
  },
  componentDidMount: function() {
    this.loadCommentsFromServer();
    // setInterval(this.loadCommentsFromServer, this.props.pollInterval)
  },
  render: function() {
    return (
      <div className="commentBox col-xs-12">
        <CommentList ref='CommentList' data={this.state.data} />
        <CommentForm url={"/anlzer/api/projects/" + project + "/comments/post/"} onCommentSubmit={this.loadCommentsFromServer} />
      </div>
    );
  }
});


ReactDOM.render(
  <CommentBox url={"/anlzer/api/projects/" + project + "/comments/"} pollInterval={3000}/>,
  document.getElementById('project-comments-box')
);
