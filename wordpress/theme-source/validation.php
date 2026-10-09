<?php
/** Read-only Gutenberg check, available only in the WPVibe draft preview. */
if ( ! defined( 'ABSPATH' ) ) { exit; }
function psy_editorial_validation_assets() {
    if ( ! is_front_page() || ! isset( $_GET['psy_validate'] ) || '-wpvibe-draft' !== substr( get_stylesheet(), -13 ) ) { return; }
    $sources = array();
    foreach ( array( 'home' => 'content/home.html', 'header' => 'parts/home-header.html', 'footer' => 'parts/home-footer.html' ) as $name => $relative ) {
        $path = get_stylesheet_directory() . '/' . $relative;
        if ( is_readable( $path ) ) { $sources[ $name ] = file_get_contents( $path ); }
    }
    wp_enqueue_script( 'psy-block-validation', get_stylesheet_directory_uri() . '/assets/js/validate-blocks.js', array( 'wp-block-library' ), filemtime( get_stylesheet_directory() . '/assets/js/validate-blocks.js' ), true );
    wp_add_inline_script( 'psy-block-validation', 'window.psyValidationSources = ' . wp_json_encode( $sources, JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT ) . ';', 'before' );
}
add_action( 'wp_enqueue_scripts', 'psy_editorial_validation_assets', 40 );
