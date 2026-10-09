<?php
/** Layout assets belong to this child theme; parent updates remain enabled. */
function psy_editorial_setup() {
    add_theme_support( 'editor-styles' );
    add_editor_style( array( 'assets/css/editor.css' ) );
    register_block_style( 'core/group', array( 'name' => 'psy-section', 'label' => 'Psyjaciele — sekcja' ) );
    register_block_style( 'core/group', array( 'name' => 'psy-rule', 'label' => 'Psyjaciele — separator' ) );
    register_block_style( 'core/columns', array( 'name' => 'psy-columns', 'label' => 'Psyjaciele — szpalty' ) );
    register_block_pattern_category( 'psyjaciele-sections', array( 'label' => 'Psyjaciele — uniwersalne sekcje' ) );
}
add_action( 'after_setup_theme', 'psy_editorial_setup', 30 );
function psy_editorial_is_section_page() {
    return is_front_page() || is_page_template( 'psyjaciele-sections' );
}
function psy_editorial_assets() {
    wp_enqueue_style( 'psy-global', get_stylesheet_directory_uri() . '/assets/css/globals.css', array(), filemtime( get_stylesheet_directory() . '/assets/css/globals.css' ) );
    if ( ! psy_editorial_is_section_page() ) { return; }
    $enqueue = json_decode( file_get_contents( get_stylesheet_directory() . '/assets/enqueue.json' ), true );
    $previous = array( 'psy-global' );
    foreach ( $enqueue['styles'] as $name ) {
        $handle = 'psy-editorial-' . $name;
        wp_enqueue_style( $handle, get_stylesheet_directory_uri() . '/assets/css/' . $name . '.css', $previous, filemtime( get_stylesheet_directory() . '/assets/css/' . $name . '.css' ) );
        $previous = array( $handle );
    }
    $previous = array();
    foreach ( $enqueue['scripts'] as $name ) {
        $handle = 'psy-editorial-' . $name;
        wp_enqueue_script( $handle, get_stylesheet_directory_uri() . '/assets/js/' . $name . '.js', $previous, filemtime( get_stylesheet_directory() . '/assets/js/' . $name . '.js' ), array( 'strategy' => 'defer', 'in_footer' => true ) );
        $previous = array( $handle );
    }
}
add_action( 'wp_enqueue_scripts', 'psy_editorial_assets', 30 );
function psy_editorial_body_class( $classes ) { if ( psy_editorial_is_section_page() ) { $classes[] = 'book-type'; $classes[] = 'psy-editorial'; } return $classes; }
add_filter( 'body_class', 'psy_editorial_body_class' );

/** Add functional image/tooltip attributes at render time. Save markup stays native. */
function psy_editorial_render_attributes( $content, $block ) {
    // Keep native editor blocks; flatten layout-only wrappers on the home frontend.
    if ( psy_editorial_is_section_page() && in_array( $block['blockName'], array( 'core/post-content', 'core/buttons' ), true ) ) {
        return preg_replace( '/^\s*<div[^>]*>([\s\S]*)<\/div>\s*$/', '$1', $content );
    }
    if ( psy_editorial_is_section_page() && 'core/button' === $block['blockName'] && in_array( 'button', explode( ' ', $block['attrs']['className'] ?? '' ), true ) && preg_match( '/<a\b[^>]*>[\s\S]*?<\/a>/', $content, $link ) ) {
        $button = new WP_HTML_Tag_Processor( $link[0] );
        if ( $button->next_tag( 'A' ) ) { $button->set_attribute( 'class', 'button' ); }
        return $button->get_updated_html();
    }
    if ( 'core/navigation' === $block['blockName'] && 'site-nav' === ( $block['attrs']['className'] ?? '' ) ) {
        $nav = new WP_HTML_Tag_Processor( $content );
        if ( $nav->next_tag( 'UL' ) ) {
            $nav->set_attribute( 'class', 'wp-block-navigation__container' );
            $nav->remove_attribute( 'id' );
            $nav->remove_attribute( 'aria-label' );
        }
        return $nav->get_updated_html();
    }
    static $config = null;
    if ( null === $config ) {
        $path = get_stylesheet_directory() . '/assets/block-config.json';
        $config = file_exists( $path ) ? json_decode( file_get_contents( $path ), true ) : array();
    }
    $class = isset( $block['attrs']['className'] ) ? $block['attrs']['className'] : '';
    if ( 'core/paragraph' === $block['blockName'] && 'psy-inline-link' === $class ) { return preg_replace( '/^\s*<p[^>]*>([\s\S]*)<\/p>\s*$/', '$1', $content ); }
    if ( ! preg_match( '/\bpsy-config-(?:[a-f0-9]{12}|\d+)\b/', $class, $match ) || empty( $config[ $match[0] ] ) || ! class_exists( 'WP_HTML_Tag_Processor' ) ) { return $content; }
    $attrs = $config[ $match[0] ];
    $processor = new WP_HTML_Tag_Processor( $content );
    if ( isset( $attrs['image'] ) ) {
        if ( $processor->next_tag( 'IMG' ) ) {
            foreach ( $attrs['image'] as $key => $value ) {
                if ( 'class' === $key ) { $value = trim( $processor->get_attribute( 'class' ) . ' ' . $value ); }
                $processor->set_attribute( $key, $value );
            }
        }
    } elseif ( $processor->next_tag() ) {
        foreach ( $attrs as $key => $value ) { $processor->set_attribute( $key, $value ); }
    }
    return $processor->get_updated_html();
}
add_filter( 'render_block', 'psy_editorial_render_attributes', 10, 2 );


/** Draft-only content preview. Published home stays editable as page 14 blocks. */
function psy_editorial_draft_home( $content, $block ) {
    if ( is_front_page() && 'core/post-content' === $block['blockName'] && '-wpvibe-draft' === substr( get_stylesheet(), -13 ) ) {
        $path = get_stylesheet_directory() . '/content/home.html';
        if ( is_readable( $path ) ) { return do_blocks( file_get_contents( $path ) ); }
    }
    return $content;
}
add_filter( 'render_block_core/post-content', 'psy_editorial_draft_home', 9, 2 );

require_once get_stylesheet_directory() . '/validation.php';
