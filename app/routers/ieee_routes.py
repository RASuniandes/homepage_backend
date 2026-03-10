from fastapi import APIRouter, Depends, Form, File, UploadFile, Query
from datetime import datetime
import requests
import logging

ieee_router = APIRouter(tags=["ieee"])
logger = logging.getLogger(__name__)

@ieee_router.get('/ieee-events')
async def get_ieee_events(
  limit: int = Query(10, ge=1, le=100),
  page: int = Query(1, ge=1),
  published: bool = Query(True),
  title: str = Query(None),
  location_type: str = Query(None, regex="^(physical|virtual|hybrid)$"),
  cancelled: bool = Query(False),
  cost: bool = Query(None),
  start_time_after: str = Query(None),  # ISO 8601 format
  start_time_before: str = Query(None),  # ISO 8601 format
  city: str = Query(None),
  tags: str = Query(None),  # comma-separated
  keywords: str = Query(None),
):
  """Fetches upcoming IEEE events from the external API with filters."""
  logger.info("Fetching IEEE events with filters")
  try:
    logger.debug("Making request to IEEE events API")
    response = requests.get(
      f'https://events.vtools.ieee.org/RST/events/api/public/v7/events/list?limit={limit}&page={page}&published={str(published).lower()}'
    )
    response.raise_for_status()
    
    api_data = response.json()
    events = api_data.get('data', [])
    total = api_data.get('total', 0)
    
    # Apply client-side filters
    events = _filter_events(
      events,
      title=title,
      location_type=location_type,
      cancelled=cancelled,
      cost=cost,
      start_time_after=start_time_after,
      start_time_before=start_time_before,
      city=city,
      tags=tags,
      keywords=keywords,
    )
    
    logger.info(f"Successfully fetched {len(events)} IEEE events")
    
    return {
      "data": {
        "events": events,
        "pagination": {
          "per_page": limit,
          "total": total,
          "pages": (total + limit - 1) // limit,
          "total_amount": total
        }
      }
    }
  except requests.RequestException as e:
    logger.error(f"Failed to fetch IEEE events: {str(e)}", exc_info=True)
    return {"error": "Failed to fetch IEEE events", "details": str(e)}


def _filter_events(events, title=None, location_type=None, cancelled=None, 
                   cost=None, start_time_after=None, start_time_before=None,
                   city=None, tags=None, keywords=None):
  """Apply filters to events list."""
  filtered = events
  
  if title:
    filtered = [e for e in filtered if title.lower() in e.get('attributes', {}).get('title', '').lower()]
  if location_type:
    filtered = [e for e in filtered if e.get('attributes', {}).get('location-type') == location_type]
  if cancelled is not None:
    filtered = [e for e in filtered if e.get('attributes', {}).get('cancelled') == cancelled]
  if cost is not None:
    filtered = [e for e in filtered if e.get('attributes', {}).get('cost') == cost]
  if start_time_after:
    filtered = [e for e in filtered if e.get('attributes', {}).get('start-time', '') >= start_time_after]
  if start_time_before:
    filtered = [e for e in filtered if e.get('attributes', {}).get('start-time', '') <= start_time_before]
  if city:
    filtered = [e for e in filtered if city.lower() in e.get('attributes', {}).get('city', '').lower()]
  if tags:
    tag_list = [t.strip() for t in tags.split(',')]
    filtered = [e for e in filtered if any(t in e.get('attributes', {}).get('tags', []) for t in tag_list)]
  if keywords:
    filtered = [e for e in filtered if keywords.lower() in e.get('attributes', {}).get('keywords', '').lower()]
  
  return filtered