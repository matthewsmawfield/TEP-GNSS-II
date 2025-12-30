#!/usr/bin/env python3
"""
Compute Planetary Events from JPL Ephemeris

This script computes accurate planetary event dates (conjunctions, oppositions)
using JPL DE432s ephemeris data. This eliminates manual transcription errors
and provides verifiable astronomical data.

Event Types:
- Mercury/Venus: Inferior Conjunctions (planet between Earth and Sun)
- Mars/Jupiter/Saturn: Oppositions (planet opposite Sun from Earth)

Author: TEP-GNSS Project
Date: 2024-12-06
"""

import numpy as np
from datetime import datetime, timedelta
from jplephem.spk import SPK
from pathlib import Path
import json

# JPL body codes
SUN = 10
MERCURY = 1
VENUS = 2
EARTH = 3
MARS = 4
JUPITER = 5
SATURN = 6

# Ephemeris file path
EPHEMERIS_PATH = Path(__file__).parent.parent.parent / "de432s.bsp"

def load_ephemeris():
    """Load the JPL ephemeris file."""
    if not EPHEMERIS_PATH.exists():
        raise FileNotFoundError(f"Ephemeris file not found: {EPHEMERIS_PATH}")
    return SPK.open(str(EPHEMERIS_PATH))


def jd_to_date(jd):
    """Convert Julian Date to datetime."""
    # J2000.0 = JD 2451545.0 = 2000-01-01 12:00:00 UTC
    j2000 = datetime(2000, 1, 1, 12, 0, 0)
    delta_days = jd - 2451545.0
    return j2000 + timedelta(days=delta_days)


def date_to_jd(dt):
    """Convert datetime to Julian Date."""
    j2000 = datetime(2000, 1, 1, 12, 0, 0)
    delta = dt - j2000
    return 2451545.0 + delta.total_seconds() / 86400.0


def get_planet_position(kernel, planet_code, jd):
    """
    Get heliocentric position of a planet at given Julian Date.
    Returns position vector in km.
    """
    # DE432s uses barycentric coordinates, need to chain:
    # Planet position relative to Sun = Planet_bary - Sun_bary
    
    # Get barycentric positions
    if planet_code == EARTH:
        # Earth-Moon barycenter (3) then Earth relative to EMB
        emb_pos = kernel[0, 3].compute(jd)
        earth_rel_emb = kernel[3, 399].compute(jd)
        planet_bary = emb_pos + earth_rel_emb
    elif planet_code == MERCURY:
        planet_bary = kernel[0, 1].compute(jd)
    elif planet_code == VENUS:
        planet_bary = kernel[0, 2].compute(jd)
    elif planet_code == MARS:
        planet_bary = kernel[0, 4].compute(jd)
    elif planet_code == JUPITER:
        planet_bary = kernel[0, 5].compute(jd)
    elif planet_code == SATURN:
        planet_bary = kernel[0, 6].compute(jd)
    else:
        raise ValueError(f"Unknown planet code: {planet_code}")
    
    # Get Sun position (barycentric)
    sun_bary = kernel[0, 10].compute(jd)
    
    # Heliocentric position
    return planet_bary - sun_bary


def compute_elongation(kernel, planet_code, jd):
    """
    Compute elongation angle (Sun-Earth-Planet angle) at given JD.
    Returns angle in degrees (0-180).
    
    For inferior planets (Mercury, Venus):
    - Elongation ~0° at inferior conjunction (planet between Earth and Sun)
    - Elongation ~0° at superior conjunction (planet behind Sun)
    - Maximum elongation varies (18-28° for Mercury, up to 47° for Venus)
    
    For superior planets (Mars, Jupiter, Saturn):
    - Elongation ~0° at conjunction (planet behind Sun)
    - Elongation ~180° at opposition (planet opposite Sun)
    """
    # Get heliocentric positions
    earth_pos = get_planet_position(kernel, EARTH, jd)
    planet_pos = get_planet_position(kernel, planet_code, jd)
    
    # Geocentric vectors
    sun_from_earth = -earth_pos  # Sun direction from Earth
    planet_from_earth = planet_pos - earth_pos  # Planet direction from Earth
    
    # Normalize
    sun_norm = sun_from_earth / np.linalg.norm(sun_from_earth)
    planet_norm = planet_from_earth / np.linalg.norm(planet_from_earth)
    
    # Angle between them (elongation)
    cos_angle = np.clip(np.dot(sun_norm, planet_norm), -1, 1)
    elongation = np.degrees(np.arccos(cos_angle))
    
    return elongation


def compute_earth_planet_distance(kernel, planet_code, jd):
    """Compute distance from Earth to planet in AU."""
    AU_KM = 149597870.7
    earth_pos = get_planet_position(kernel, EARTH, jd)
    planet_pos = get_planet_position(kernel, planet_code, jd)
    dist_km = np.linalg.norm(planet_pos - earth_pos)
    return dist_km / AU_KM


def find_inferior_conjunctions(kernel, planet_code, start_year, end_year):
    """
    Find inferior conjunctions for Mercury or Venus.
    
    Inferior conjunction = planet between Earth and Sun
    Characterized by:
    1. Elongation near minimum (close to 0°)
    2. Planet closer to Earth than Sun (distance < 1 AU for Venus, < 1 AU for Mercury)
    
    We search for local minima in elongation where planet is closer than the Sun.
    """
    if planet_code not in [MERCURY, VENUS]:
        raise ValueError("Inferior conjunctions only for Mercury/Venus")
    
    planet_name = "Mercury" if planet_code == MERCURY else "Venus"
    
    # Synodic periods (approximate, for search spacing)
    synodic_period = 116 if planet_code == MERCURY else 584  # days
    
    events = []
    
    # Search with daily resolution
    start_jd = date_to_jd(datetime(start_year, 1, 1))
    end_jd = date_to_jd(datetime(end_year + 1, 1, 1))
    
    jd = start_jd
    prev_elongation = compute_elongation(kernel, planet_code, jd)
    prev_distance = compute_earth_planet_distance(kernel, planet_code, jd)
    
    jd += 1
    curr_elongation = compute_elongation(kernel, planet_code, jd)
    curr_distance = compute_earth_planet_distance(kernel, planet_code, jd)
    
    while jd < end_jd:
        jd += 1
        next_elongation = compute_elongation(kernel, planet_code, jd)
        next_distance = compute_earth_planet_distance(kernel, planet_code, jd)
        
        # Check for local minimum in elongation
        if curr_elongation < prev_elongation and curr_elongation < next_elongation:
            # This is a conjunction (either inferior or superior)
            # Inferior = planet closer than 1 AU
            # Superior = planet farther than 1 AU
            
            if curr_distance < 1.0:  # Inferior conjunction
                # Refine to find exact minimum
                best_jd = jd - 1
                best_elong = curr_elongation
                
                # Fine search (0.01 day = ~15 min resolution)
                for delta in np.arange(-1, 1, 0.01):
                    test_jd = jd - 1 + delta
                    test_elong = compute_elongation(kernel, planet_code, test_jd)
                    if test_elong < best_elong:
                        best_elong = test_elong
                        best_jd = test_jd
                
                event_date = jd_to_date(best_jd)
                events.append({
                    'date': event_date,
                    'jd': best_jd,
                    'elongation': best_elong,
                    'distance_au': compute_earth_planet_distance(kernel, planet_code, best_jd),
                    'type': 'inferior_conjunction',
                    'planet': planet_name
                })
        
        prev_elongation = curr_elongation
        prev_distance = curr_distance
        curr_elongation = next_elongation
        curr_distance = next_distance
    
    return events


def find_oppositions(kernel, planet_code, start_year, end_year):
    """
    Find oppositions for Mars, Jupiter, or Saturn.
    
    Opposition = planet opposite the Sun from Earth
    Characterized by elongation ~180°
    """
    if planet_code not in [MARS, JUPITER, SATURN]:
        raise ValueError("Oppositions only for Mars/Jupiter/Saturn")
    
    planet_names = {MARS: "Mars", JUPITER: "Jupiter", SATURN: "Saturn"}
    planet_name = planet_names[planet_code]
    
    events = []
    
    # Search with daily resolution
    start_jd = date_to_jd(datetime(start_year, 1, 1))
    end_jd = date_to_jd(datetime(end_year + 1, 1, 1))
    
    jd = start_jd
    prev_elongation = compute_elongation(kernel, planet_code, jd)
    
    jd += 1
    curr_elongation = compute_elongation(kernel, planet_code, jd)
    
    while jd < end_jd:
        jd += 1
        next_elongation = compute_elongation(kernel, planet_code, jd)
        
        # Check for local maximum in elongation (opposition)
        if curr_elongation > prev_elongation and curr_elongation > next_elongation:
            if curr_elongation > 170:  # Must be near 180° for opposition
                # Refine to find exact maximum
                best_jd = jd - 1
                best_elong = curr_elongation
                
                for delta in np.arange(-1, 1, 0.01):
                    test_jd = jd - 1 + delta
                    test_elong = compute_elongation(kernel, planet_code, test_jd)
                    if test_elong > best_elong:
                        best_elong = test_elong
                        best_jd = test_jd
                
                event_date = jd_to_date(best_jd)
                events.append({
                    'date': event_date,
                    'jd': best_jd,
                    'elongation': best_elong,
                    'distance_au': compute_earth_planet_distance(kernel, planet_code, best_jd),
                    'type': 'opposition',
                    'planet': planet_name
                })
        
        prev_elongation = curr_elongation
        curr_elongation = next_elongation
    
    return events


def format_events_for_code(events, event_type):
    """Format events as Python code for inclusion in analysis scripts."""
    lines = []
    
    for event in events:
        date_str = event['date'].strftime('%Y-%m-%d')
        planet = event['planet'].lower()
        year = event['date'].year
        month = event['date'].strftime('%m')
        
        if event['type'] == 'inferior_conjunction':
            name = f"{planet}_{year}_{month}"
            desc = f"{event['planet']} Inferior Conjunction {event['date'].strftime('%B %Y')}"
        else:
            name = f"{planet}_{year}"
            desc = f"{event['planet']} Opposition {event['date'].strftime('%B %Y')}"
        
        lines.append(
            f"            {{'name': '{name}', 'date': pd.to_datetime('{date_str}'), "
            f"'description': '{desc}'}},"
        )
    
    return '\n'.join(lines)


def main():
    """Compute and display all planetary events for TEP analysis."""
    print("=" * 80)
    print("PLANETARY EVENTS FROM JPL DE432s EPHEMERIS")
    print("=" * 80)
    
    kernel = load_ephemeris()
    print(f"Loaded ephemeris: {EPHEMERIS_PATH}")
    
    start_year = 2000
    end_year = 2025
    
    all_events = {}
    
    # Mercury Inferior Conjunctions
    print(f"\n{'='*60}")
    print("MERCURY INFERIOR CONJUNCTIONS (2000-2025)")
    print("="*60)
    mercury_events = find_inferior_conjunctions(kernel, MERCURY, start_year, end_year)
    all_events['Mercury'] = mercury_events
    print(f"Found {len(mercury_events)} events:")
    for e in mercury_events:
        print(f"  {e['date'].strftime('%Y-%m-%d')} (elongation: {e['elongation']:.1f}°, distance: {e['distance_au']:.3f} AU)")
    
    # Venus Inferior Conjunctions
    print(f"\n{'='*60}")
    print("VENUS INFERIOR CONJUNCTIONS (2000-2025)")
    print("="*60)
    venus_events = find_inferior_conjunctions(kernel, VENUS, start_year, end_year)
    all_events['Venus'] = venus_events
    print(f"Found {len(venus_events)} events:")
    for e in venus_events:
        print(f"  {e['date'].strftime('%Y-%m-%d')} (elongation: {e['elongation']:.1f}°, distance: {e['distance_au']:.3f} AU)")
    
    # Mars Oppositions
    print(f"\n{'='*60}")
    print("MARS OPPOSITIONS (2000-2025)")
    print("="*60)
    mars_events = find_oppositions(kernel, MARS, start_year, end_year)
    all_events['Mars'] = mars_events
    print(f"Found {len(mars_events)} events:")
    for e in mars_events:
        print(f"  {e['date'].strftime('%Y-%m-%d')} (elongation: {e['elongation']:.1f}°, distance: {e['distance_au']:.3f} AU)")
    
    # Jupiter Oppositions
    print(f"\n{'='*60}")
    print("JUPITER OPPOSITIONS (2000-2025)")
    print("="*60)
    jupiter_events = find_oppositions(kernel, JUPITER, start_year, end_year)
    all_events['Jupiter'] = jupiter_events
    print(f"Found {len(jupiter_events)} events:")
    for e in jupiter_events:
        print(f"  {e['date'].strftime('%Y-%m-%d')} (elongation: {e['elongation']:.1f}°, distance: {e['distance_au']:.3f} AU)")
    
    # Saturn Oppositions
    print(f"\n{'='*60}")
    print("SATURN OPPOSITIONS (2000-2025)")
    print("="*60)
    saturn_events = find_oppositions(kernel, SATURN, start_year, end_year)
    all_events['Saturn'] = saturn_events
    print(f"Found {len(saturn_events)} events:")
    for e in saturn_events:
        print(f"  {e['date'].strftime('%Y-%m-%d')} (elongation: {e['elongation']:.1f}°, distance: {e['distance_au']:.3f} AU)")
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print("="*80)
    total = sum(len(v) for v in all_events.values())
    print(f"Total events: {total}")
    for planet, events in all_events.items():
        print(f"  {planet}: {len(events)} events")
    
    # Output as Python code
    print(f"\n{'='*80}")
    print("PYTHON CODE FOR step_2_2_code_longspan.py")
    print("="*80)
    
    print("\n# Mercury Inferior Conjunctions (JPL DE432s verified)")
    print("mercury_events = [")
    print(format_events_for_code(mercury_events, 'inferior_conjunction'))
    print("]")
    
    print("\n# Venus Inferior Conjunctions (JPL DE432s verified)")
    print("venus_events = [")
    print(format_events_for_code(venus_events, 'inferior_conjunction'))
    print("]")
    
    print("\n# Mars Oppositions (JPL DE432s verified)")
    print("mars_events = [")
    print(format_events_for_code(mars_events, 'opposition'))
    print("]")
    
    print("\n# Jupiter Oppositions (JPL DE432s verified)")
    print("jupiter_events = [")
    print(format_events_for_code(jupiter_events, 'opposition'))
    print("]")
    
    print("\n# Saturn Oppositions (JPL DE432s verified)")
    print("saturn_events = [")
    print(format_events_for_code(saturn_events, 'opposition'))
    print("]")
    
    # Save to JSON for reference
    output_data = {}
    for planet, events in all_events.items():
        output_data[planet] = [
            {
                'date': e['date'].strftime('%Y-%m-%d'),
                'elongation': round(e['elongation'], 2),
                'distance_au': round(e['distance_au'], 4),
                'type': e['type']
            }
            for e in events
        ]
    
    output_file = Path(__file__).parent.parent.parent / "results" / "outputs" / "code_longspan" / "planetary_events_jpl.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    print(f"\nSaved to: {output_file}")
    
    return all_events


if __name__ == "__main__":
    main()
