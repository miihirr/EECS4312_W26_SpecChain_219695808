# Specification — Manual Pipeline
**Application:** Headspace (com.getsomeheadspace.android)
**Pipeline:** Manual
**Author:** Mihirkumar Patel (219695808)
**Source Dataset:** data/reviews_clean.jsonl (200 reviews)

---

## Requirement ID: FR1
- **Description:** The system shall continue playing Sleepcast and sleep-sound audio without interruption when the device screen locks or when a notification is received, so long as the user has not manually paused playback.
- **Source Persona:** The Insomniac Sleepcast Listener (P1)
- **Traceability:** Derived from review group G1 (sleep content quality and Sleepcast experience)
- **Acceptance Criteria:** Given a user is playing a Sleepcast, when the device screen locks or a notification arrives, then audio playback shall continue uninterrupted at the same volume and position as before the screen-lock or notification event.

---

## Requirement ID: FR2
- **Description:** The system shall accurately honour the user-configured sleep timer, stopping audio playback with a 30-second fade-out at the exact configured time, with a tolerance of no more than 60 seconds.
- **Source Persona:** The Insomniac Sleepcast Listener (P1)
- **Traceability:** Derived from review group G1 (sleep content quality and Sleepcast experience)
- **Acceptance Criteria:** Given a user has set the sleep timer to 45 minutes, when 45 minutes of playback have elapsed, then the audio volume shall begin a 30-second fade-out and playback shall cease completely within 46 minutes of the timer being set.

---

## Requirement ID: FR3
- **Description:** The system shall make all downloaded Sleepcast and sleep-sound content fully playable in airplane mode without making any network requests.
- **Source Persona:** The Insomniac Sleepcast Listener (P1)
- **Traceability:** Derived from review group G1 (sleep content quality and Sleepcast experience)
- **Acceptance Criteria:** Given a user has downloaded a Sleepcast while connected to the internet, when the device is placed in airplane mode and the user opens and plays that Sleepcast, then playback shall begin within 5 seconds and audio shall play completely without buffering or error.

---

## Requirement ID: FR4
- **Description:** The system shall not reset a user's meditation streak counter as a result of server-side failures, network outages, or application maintenance windows; any streak affected by such events shall be automatically restored or restorable via customer support.
- **Source Persona:** The Structured Course Meditator (P2)
- **Traceability:** Derived from review group G2 (guided meditation, courses, and Andy Puddicombe experience)
- **Acceptance Criteria:** Given a user has an active streak and a server outage occurs on a day the user had already completed their session, when the system recovers from the outage, then the streak counter shall reflect the completed session and shall not have been decremented.

---

## Requirement ID: FR5
- **Description:** The system shall provide a shortened session variant for every course session, allowing users to complete a condensed version of at least 5 minutes when the full-length session is not practical.
- **Source Persona:** The Structured Course Meditator (P2)
- **Traceability:** Derived from review group G2 (guided meditation, courses, and Andy Puddicombe experience)
- **Acceptance Criteria:** Given a user opens any session within a Headspace course, when they view the session options, then a session-length selector shall be present showing at minimum a 5-minute short variant and the original length, and selecting the short variant shall play a condensed but complete version.

---

## Requirement ID: FR6
- **Description:** The system shall update content recommendations whenever a user completes a course, so that the completed course is no longer surfaced as a primary daily recommendation and higher-level content is promoted.
- **Source Persona:** The Structured Course Meditator (P2)
- **Traceability:** Derived from review group G2 (guided meditation, courses, and Andy Puddicombe experience)
- **Acceptance Criteria:** Given a user has marked a course as complete, when they next open the app, then the home screen recommendation feed shall not display that completed course as the primary suggestion, and at least one course of equal or greater difficulty shall be surfaced instead.

---

## Requirement ID: FR7
- **Description:** The system shall dispatch a push notification and email to the user at least 7 calendar days before their subscription auto-renews, clearly stating the renewal date, the charge amount, and providing a direct link to subscription management.
- **Source Persona:** The Cost-Conscious Subscriber (P3)
- **Traceability:** Derived from review group G3 (subscription cost, paywalls, and billing issues)
- **Acceptance Criteria:** Given a user's subscription is set to auto-renew in 7 days, when the system processes upcoming renewals, then a push notification and email shall be dispatched containing the renewal date, charge amount, and a tappable link that navigates directly to the subscription management screen.

---

## Requirement ID: FR8
- **Description:** The system shall make the subscription cancellation option accessible within 3 navigation taps from the app's home screen, without requiring the user to visit an external website or contact customer support.
- **Source Persona:** The Cost-Conscious Subscriber (P3)
- **Traceability:** Derived from review group G3 (subscription cost, paywalls, and billing issues)
- **Acceptance Criteria:** Given a subscribed user who wishes to cancel, when they navigate from the home screen through Account and then Subscription, then a clearly labelled Cancel Subscription option shall be present and activatable without leaving the app.

---

## Requirement ID: FR9
- **Description:** The system shall maintain seamless audio playback when the Headspace app is backgrounded on Android, using a foreground service to prevent the OS from terminating audio.
- **Source Persona:** The Frustrated Android User (P4)
- **Traceability:** Derived from review group G4 (technical bugs, crashes, and background audio failures)
- **Acceptance Criteria:** Given a user is playing a guided meditation and switches to another app, when Headspace enters the background, then audio shall continue playing without pause or interruption for the full remaining session duration.

---

## Requirement ID: FR10
- **Description:** The system shall preserve all user account data — including session history, streak count, and course progress — in cloud storage and restore it completely when the user signs in on a new device.
- **Source Persona:** The Frustrated Android User (P4)
- **Traceability:** Derived from review group G4 (technical bugs, crashes, and background audio failures)
- **Acceptance Criteria:** Given a user signs in to their Headspace account on a new Android device, when the app completes its initial sync, then the session history, streak count, and course completion status shall match the values from their previous device within 2 minutes of login.

---

## Requirement ID: FR11
- **Description:** The system shall incorporate each mood check-in response into the daily content recommendation within the same app session, surfacing at least one piece of content explicitly labelled as relevant to the reported mood.
- **Source Persona:** The Long-Term Personalization Seeker (P5)
- **Traceability:** Derived from review group G5 (content variety, personalization, and feature breadth)
- **Acceptance Criteria:** Given a user completes the mood check-in and selects a mood such as anxious or tired, when the recommendation feed loads after the check-in, then the first recommended item shall be tagged with a label indicating why it was recommended based on the stated mood.

---

## Requirement ID: FR12
- **Description:** The system shall add at least 2 new Sleepcast episodes to the library per calendar month and shall surface newly added content prominently on the home screen for a minimum of 14 days following publication.
- **Source Persona:** The Long-Term Personalization Seeker (P5)
- **Traceability:** Derived from review group G5 (content variety, personalization, and feature breadth)
- **Acceptance Criteria:** Given a user has been subscribed for more than 6 months, when they open the Sleep section, then at least 2 Sleepcasts published within the current calendar month shall be visible in a New section on the Sleep home page.

---

## Requirement ID: FR13
- **Description:** The system shall allow users to flag a recommendation as not relevant, and shall suppress that flagged item from the user's recommendation feed for a minimum of 30 days following the flag.
- **Source Persona:** The Long-Term Personalization Seeker (P5)
- **Traceability:** Derived from review group G5 (content variety, personalization, and feature breadth)
- **Acceptance Criteria:** Given a user sees a recommended session and taps Not for me, when the system records the flag, then that session shall not appear in the recommendation feed for at least the next 30 days.

---

## Requirement ID: FR14
- **Description:** The system shall support a tablet landscape layout on Android devices with screens of 7 inches or larger, presenting a two-column interface that fully utilises the available screen area.
- **Source Persona:** The Frustrated Android User (P4)
- **Traceability:** Derived from review group G4 (technical bugs, crashes, and background audio failures)
- **Acceptance Criteria:** Given a user is running Headspace on an Android tablet with a screen diagonal of 7 inches or larger, when the device is held in landscape orientation, then the UI shall reflow into a landscape two-column layout without truncation or portrait-only rendering.
