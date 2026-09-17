# Product Brief: Your Next Adventure

## Executive Summary

Your Next Adventure is a website that helps people plan their next hike in nature. Instead of digging through general maps or large trail databases, the user simply enters where they want to go, how much time they have, and what kind of experience they're looking for, whether that is a demanding summit hike, a relaxed walk in the woods, or something in between. The service responds with concrete suggestions: a route on a map, time estimates, and practical tips.

What sets Your Next Adventure apart is that it gets smarter the more it's used. With a user account, past trips are saved, and the system learns what the user actually enjoyed and how they experienced the difficulty level, not just what an objective trail map says about elevation gain and length. Over time, this produces suggestions tailored to the individual, not just the location.

## The Problem

Planning a trip in nature often takes more time than the trip itself should require. People generally know roughly where they want to go and how much time they have, but finding a route that actually fits means searching through multiple sources such as trail maps, blogs, AllTrails, ut.no, and Google Maps to get the right length, the right type of experience, and the right difficulty level for that particular day.

Today, people solve this by spending a lot of time on research, asking friends, or simply picking a trip they already know because it feels safer than searching. The consequence is that people either spend time they don't have, or end up with trips that don't match what they actually wanted that day: too easy, too hard, or simply the wrong type of nature. None of the existing tools take into account who the user is and what they've liked before, since they are static databases rather than something that learns from you.

## The Solution

Your Next Adventure lets the user describe the trip they want, including location, available time, and desired type of experience such as a summit hike, a forest walk, or a trip with a view, and get concrete, ready-made suggestions back: a route shown on a map, an estimated time, and relevant tips for the trip, including clothing recommendations based on the weather forecast for the day of the trip.

With login, users can save past trips. The system uses this history, together with the user's own rating of how easy or hard a trip actually was, to understand the user's preferences and accuracy regarding difficulty level. The next time the user asks for a suggestion, the recommendation is tailored to them instead of being a generic list of trips in the area.

## What Makes This Different

Trail databases and map tools that exist today, such as ut.no, AllTrails, and Google Maps, are good at showing what's available in a place, but they are static and return the same result no matter who's asking. Your Next Adventure's advantage is personalization based on actual user history and self-reported experience, combined with the ability for the user to express what they want in plain language, such as "a relaxed forest walk for a couple of hours," instead of filtering through lists.

We want to be honest about what the advantage actually is: it doesn't lie in a unique technical invention, but in how well we combine existing data, such as maps and trail information, with the user's own history and feedback, and in how quickly and accurately we can deliver it as a coherent experience.

## Who This Serves

Primary user: people who enjoy hiking in nature, ranging from beginners who are unsure what they can handle to experienced hikers who want quick, accurate suggestions without spending time on research. What they have in common is that they roughly know what they want in terms of time, place, and type of experience, but not necessarily the specific route. Success for them means getting a suggestion they trust and actually use, one that becomes better tailored to them the more they use the service.

Secondary user: tourists or newcomers who don't know the area well, and who need concrete suggestions tailored to how much time they have available.

## Success Criteria

- A user can enter location, time, and desired type of trip, and get a concrete suggestion with a map, time estimate, and tips.
- Users can create an account and save completed trips.
- Suggestions become noticeably more accurate for a user with trip history than for a new user, demonstrating that personalization works.
- Test users rate the suggestions as relevant and the perceived difficulty level as correctly assessed, measured through simple feedback after the trip.
- The project delivers a working demo that covers the core flow: input, suggestion, saving, and improved suggestion.

## Scope

**Included in the first version:**
- Input for location, available time, and desired trip type or experience
- AI-generated trip suggestions with a map, time estimate, and tips
- Weather-based clothing tips for the trip suggestion, retrieved from Yr/MET's weather forecast API for the trip's location and time
- User account with login
- Saving of past trips and simple feedback, such as perceived difficulty level and whether the user liked or disliked the trip
- Basic personalization of suggestions based on saved history

**Explicitly out of scope for the first version:**
- Weather forecasts as a standalone notification service, such as push notifications or warning messages; weather is used only as input to the trip suggestion, not as an independent notification product
- Precise terrain or trail condition reports covering snow, ice, or mud, since this is too imprecise to promise in v1 and will be considered later
- Mobile app, since the first version will be a website only
- Social features, such as sharing, following other users, or commenting
- Offline GPS navigation during the trip
- Booking and logistics, such as accommodation, transport, or gear rental
- Support for languages beyond Norwegian and English

## Vision

In two to three years, Your Next Adventure is the first place people turn to when planning a trip in nature, not because it has the most trails in its database, but because it knows the user well enough to suggest exactly the trip they need that day. Personalization has become so accurate that users trust the suggestions without question, and the service has expanded to more regions and, over time, more types of outdoor activities than hiking, such as skiing, cycling, and paddling, always with the same core idea: understand the user, not just the place.
