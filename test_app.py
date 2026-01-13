"""
Test suite for Dash sales visualization app.

This module contains automated tests to verify that the Dash app
correctly renders all required UI components:
1. Header/title presence
2. Line chart visualization
3. Region picker radio buttons
"""

import pytest
from dash import html, dcc
from app import app


def find_component_by_id(component, target_id):
    """Recursively search for a Dash component by its ID."""
    # Check if this component has the target ID
    if hasattr(component, 'id'):
        # Dash components can have id as attribute or in props
        component_id = getattr(component, 'id', None)
        if component_id == target_id:
            return component
    
    # Check children
    if hasattr(component, 'children'):
        children = component.children
        if children is None:
            return None
        
        # Handle list of children
        if isinstance(children, list):
            for child in children:
                if child is not None:
                    result = find_component_by_id(child, target_id)
                    if result is not None:
                        return result
        # Handle single child
        elif children is not None:
            result = find_component_by_id(children, target_id)
            if result is not None:
                return result
    
    return None


def find_component_by_type_and_attr(component, component_type, **kwargs):
    """Recursively search for a component by type and attributes."""
    # Check if this is the component type we're looking for
    if isinstance(component, component_type):
        # Check if it matches all search criteria
        matches = True
        for key, value in kwargs.items():
            attr_value = getattr(component, key, None)
            if attr_value != value:
                matches = False
                break
        if matches:
            return component
    
    # Check children
    if hasattr(component, 'children'):
        children = component.children
        if children is None:
            return None
        
        # Handle list of children
        if isinstance(children, list):
            for child in children:
                if child is not None:
                    result = find_component_by_type_and_attr(child, component_type, **kwargs)
                    if result is not None:
                        return result
        # Handle single child
        elif children is not None:
            result = find_component_by_type_and_attr(children, component_type, **kwargs)
            if result is not None:
                return result
    
    return None


class TestDashApp:
    """Test class for Dash application components."""
    
    def test_header_present(self):
        """
        Test that the header/title 'Pink Morsel Sales Analysis' is present.
        
        Verifies:
        - H1 element with className 'header-title' exists in layout
        - Header text matches expected value
        """
        # Get the app layout
        layout = app.layout
        
        # Find H1 element with className 'header-title'
        header = find_component_by_type_and_attr(layout, html.H1, className='header-title')
        
        # Assert header exists
        assert header is not None, "Header element with className 'header-title' not found in layout"
        
        # Assert header text matches expected value
        assert header.children == 'Pink Morsel Sales Analysis', \
            f"Expected header text 'Pink Morsel Sales Analysis', but got '{header.children}'"
    
    def test_chart_rendered(self):
        """
        Test that the line chart visualization is rendered.
        
        Verifies:
        - Graph component with id 'sales-chart' exists in the layout
        - Component is properly configured
        """
        # Get the app layout
        layout = app.layout
        
        # Find Graph component with id 'sales-chart'
        chart = find_component_by_id(layout, 'sales-chart')
        
        # Assert chart component exists
        assert chart is not None, "Chart component with id 'sales-chart' not found in layout"
        
        # Assert it's a Graph component
        assert isinstance(chart, dcc.Graph), \
            f"Expected dcc.Graph component, but got {type(chart).__name__}"
        
        # Assert it has the correct ID
        assert chart.id == 'sales-chart', \
            f"Expected chart id to be 'sales-chart', but got '{chart.id}'"
    
    def test_region_picker_present(self):
        """
        Test that the region picker (radio buttons) is present.
        
        Verifies:
        - RadioItems component with id 'region-filter' exists
        - Component has the expected options (All, North, East, South, West)
        - Default value is 'All'
        """
        # Get the app layout
        layout = app.layout
        
        # Find RadioItems component with id 'region-filter'
        radio_filter = find_component_by_id(layout, 'region-filter')
        
        # Assert radio filter component exists
        assert radio_filter is not None, \
            "Region filter component with id 'region-filter' not found in layout"
        
        # Assert it's a RadioItems component
        assert isinstance(radio_filter, dcc.RadioItems), \
            f"Expected dcc.RadioItems component, but got {type(radio_filter).__name__}"
        
        # Assert it has the correct ID
        assert radio_filter.id == 'region-filter', \
            f"Expected radio filter id to be 'region-filter', but got '{radio_filter.id}'"
        
        # Verify expected options are present
        expected_options = ['All', 'North', 'East', 'South', 'West']
        assert hasattr(radio_filter, 'options'), "RadioItems component missing 'options' attribute"
        
        # Extract option values
        option_values = [opt['value'] if isinstance(opt, dict) else opt 
                        for opt in radio_filter.options]
        
        # Assert all expected options are present
        for expected_option in expected_options:
            assert expected_option in option_values, \
                f"Expected option '{expected_option}' not found in radio buttons. " \
                f"Found options: {option_values}"
        
        # Verify default value is 'All'
        assert hasattr(radio_filter, 'value'), "RadioItems component missing 'value' attribute"
        assert radio_filter.value == 'All', \
            f"Expected default value to be 'All', but got '{radio_filter.value}'"
