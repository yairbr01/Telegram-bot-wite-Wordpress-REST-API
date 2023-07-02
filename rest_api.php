<?php

add_action( 'rest_api_init', function() {
  register_rest_route( 'news-ticker/v1', '/add', [
    'methods' => 'POST',
    'callback' => 'news_ticker_add_new',
    'permission_callback' => 'restCheckUser',
  ] );
} );

function restCheckUser(WP_REST_Request $request) {
    if ('token_for_rest_api' === $request->get_param('token')) {
         return true;
    }
    return false;
}

function news_ticker_add_new( $request ) {
	
  	$params = wp_parse_args( $request->get_params(), [
    	'title' => '',
		'media_id' => '',
    	'video' => '',
  	] );	
	
	$title = $params['title'];
	$author_name = $params['author_name'];
	$media_id = $params['media_id'];
	$is_video = $params['video'];
	
	// publish post on website
	$post_id = wp_insert_post( array (
		'post_type' => 'news-ticker',
		'post_title' => $title,
		'post_status' => 'publish',
		'post_author' => '1',
	) );
		
	if ( $media_id != 0 ) {
		
		// if this is video
		if ( $is_video == "true" ) {
			update_post_meta( $post_id, 'video', $media_id );
		} else {
			// if this is image
			update_post_meta( $post_id, 'image', $media_id );
		}
		
	} 
}

?>
