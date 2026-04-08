# Specification — Hybrid Pipeline
**Application:** Headspace (com.getsomeheadspace.android)
**Pipeline:** Hybrid (automated output refined manually)
**Author:** Mihirkumar Patel (219695808)
**Source Dataset:** data/reviews_clean.jsonl (200 reviews)

---

## Requirement ID: FR_hybrid_1
- **Description:** The system shall maintain uninterrupted audio playback when the device screen locks during a Sleepcast or sleep-sound session, using a persistent background audio service that survives screen lock and incoming notifications.
- **Source Persona:** The Wind-Down Routine Builder (PH1)
- **Traceability:** Derived from review groups G1 and H1 (Sleepcast and sleep audio effectiveness)
- **Acceptance Criteria:** Given a user is playing a Sleepcast and locks their device screen, when the screen goes dark, then audio playback shall continue at the configured volume for the full session duration without requiring the user to unlock the device.

---

## Requirement ID: FR_hybrid_2
- **Description:** The system shall loop ambient audio or transition to a continuous ambient soundscape at the conclusion of a Sleepcast narrative, preventing silence that could awaken a user who has fallen asleep during the content.
- **Source Persona:** The Wind-Down Routine Builder (PH1)
- **Traceability:** Derived from review groups G1 and H1 (Sleepcast and sleep audio effectiveness)
- **Acceptance Criteria:** Given a user is listening to a Sleepcast with no sleep timer set, when the narration portion ends, then ambient background audio shall continue to play at a consistent volume until the user manually stops playback or a timer (if set) expires.

---

## Requirement ID: FR_hybrid_3
- **Description:** The system shall provide a sleep timer that operates with a maximum deviation of 30 seconds from the configured stop time and shall not deactivate earlier than the configured time under normal device operating conditions.
- **Source Persona:** The Wind-Down Routine Builder (PH1)
- **Traceability:** Derived from review groups G1 and H1 (Sleepcast and sleep audio effectiveness)
- **Acceptance Criteria:** Given a sleep timer is configured for 45 minutes, when 45 minutes have elapsed from the moment the timer was started, then playback shall stop within the range of 45 to 45.5 minutes, and shall not have stopped any earlier than 44.5 minutes.

---

## Requirement ID: FR_hybrid_4
- **Description:** The system shall present users who have completed beginner courses with a clearly surfaced pathway to intermediate content, including a dedicated section and guided next-step recommendations based on completed course history.
- **Source Persona:** The Evidence-Seeking Wellness Convert (PH2)
- **Traceability:** Derived from review groups G2 and H2 (guided meditation quality and course progression)
- **Acceptance Criteria:** Given a user has completed the 10-day Basics course, when they visit the home screen, then a Continue your journey section shall appear containing at least 3 courses tagged at the intermediate level and relevant to the completed course theme.

---

## Requirement ID: FR_hybrid_5
- **Description:** The system shall display the psychological rationale or technique description for each guided meditation session, accessible via a clearly labelled About section within the session details screen.
- **Source Persona:** The Evidence-Seeking Wellness Convert (PH2)
- **Traceability:** Derived from review groups G2 and H2 (guided meditation quality and course progression)
- **Acceptance Criteria:** Given a user opens any guided meditation session detail screen, when the session is displayed, then an About or Why this works section shall be visible containing a 2–4 sentence description of the meditation technique and the evidence base for the approach.

---

## Requirement ID: FR_hybrid_6
- **Description:** The system shall publish a new guest teacher pack at least once per quarter and shall notify existing subscribers via in-app notification when new teacher content becomes available.
- **Source Persona:** The Evidence-Seeking Wellness Convert (PH2)
- **Traceability:** Derived from review groups G2 and H2 (guided meditation quality and course progression)
- **Acceptance Criteria:** Given a new guest teacher pack is published, when the pack is made live, then an in-app notification shall appear for all premium subscribers within 24 hours of publication, and the pack shall be surfaced on the home screen in a New from Headspace section.

---

## Requirement ID: FR_hybrid_7
- **Description:** The system shall provide a minimum 14-day free trial for new users that includes access to at least one session from every major content category, enabling informed subscription decisions before billing begins.
- **Source Persona:** The Value-Evaluating Subscriber (PH3)
- **Traceability:** Derived from review groups G3 and H3 (subscription value, paywalls, and cancellation experience)
- **Acceptance Criteria:** Given a new user registers and starts the free trial, when they browse the app during the trial period, then sessions from Sleep, Meditation, Focus, and Move categories shall all be accessible without a subscription paywall prompt, and billing shall not commence until the 15th day.

---

## Requirement ID: FR_hybrid_8
- **Description:** The system shall send an advance renewal notification to the user at least 7 days before the subscription auto-renews, and shall provide a direct in-app link to the cancellation screen within the notification.
- **Source Persona:** The Value-Evaluating Subscriber (PH3)
- **Traceability:** Derived from review groups G3 and H3 (subscription value, paywalls, and cancellation experience)
- **Acceptance Criteria:** Given a user's subscription is 7 days from auto-renewal, when the system generates the reminder, then a push notification shall be delivered containing the renewal date, the charge amount, and a deep-link that opens the Subscription Management screen directly.

---

## Requirement ID: FR_hybrid_9
- **Description:** The system shall synchronise all user account data — including session history, streaks, course progress, and downloaded content metadata — to cloud storage in real time and restore it fully on first sign-in from a new device.
- **Source Persona:** The Data-Loss-Averse Power User (PH4)
- **Traceability:** Derived from review groups G4 and H4 (technical reliability and platform-specific bugs)
- **Acceptance Criteria:** Given a user signs in to Headspace on a new device after factory-resetting their previous device, when they complete authentication, then within 3 minutes the new device shall display the same session count, streak value, and course completion state as existed on the previous device before reset.

---

## Requirement ID: FR_hybrid_10
- **Description:** The system shall provide a customer support mechanism that allows users to request restoration of a streak that was decremented due to a verified server-side incident, with resolution guaranteed within 5 business days.
- **Source Persona:** The Data-Loss-Averse Power User (PH4)
- **Traceability:** Derived from review groups G4 and H4 (technical reliability and platform-specific bugs)
- **Acceptance Criteria:** Given a user submits a streak restoration request referencing a server incident date within their account history, when the support team verifies the incident, then the streak value shall be corrected and the user notified of the restoration within 5 business days.

---

## Requirement ID: FR_hybrid_11
- **Description:** The system shall use mood check-in responses to directly modify the content shown in the daily recommendation section, surfacing content tagged to the stated mood before any other content.
- **Source Persona:** The Life-Stage-Specific Content Searcher (PH5)
- **Traceability:** Derived from review groups G5 and H5 (personalization depth and content breadth)
- **Acceptance Criteria:** Given a user completes the mood check-in and reports feeling stressed, when the home screen recommendation section loads, then at least the top 2 recommended items shall be tagged as relevant for stress and shall have been promoted ahead of any items not matching the reported mood.

---

## Requirement ID: FR_hybrid_12
- **Description:** The system shall provide each specialised content category (grief, chronic pain, parenting, ADHD) with a minimum library of 15 individual sessions, ensuring depth sufficient for a multi-week focused practice.
- **Source Persona:** The Life-Stage-Specific Content Searcher (PH5)
- **Traceability:** Derived from review groups G5 and H5 (personalization depth and content breadth)
- **Acceptance Criteria:** Given a user navigates to any specialised content category such as Grief, Parenting, or ADHD Focus, when the category page loads, then at least 15 distinct sessions shall be listed, each with a unique title and description.

---

## Requirement ID: FR_hybrid_13
- **Description:** The system shall provide an in-app content request feature allowing users to submit topic suggestions, and shall acknowledge each submission with a confirmation message and an estimated review timeline.
- **Source Persona:** The Life-Stage-Specific Content Searcher (PH5)
- **Traceability:** Derived from review groups G5 and H5 (personalization depth and content breadth)
- **Acceptance Criteria:** Given a user navigates to Settings and selects Request Content, when they submit a topic suggestion, then the system shall display a confirmation screen acknowledging the submission and stating the review timeline within 2 weeks.

---

## Requirement ID: FR_hybrid_14
- **Description:** The system shall maintain audio playback in the background on Android without interruption when the user navigates to another app, by running audio within a foreground service that survives standard OS process management.
- **Source Persona:** The Data-Loss-Averse Power User (PH4)
- **Traceability:** Derived from review groups G4 and H4 (technical reliability and platform-specific bugs)
- **Acceptance Criteria:** Given a user is playing any Headspace audio session and switches to a another app for up to 30 minutes, when they return to the Headspace app, then the audio shall have played uninterrupted for the full duration they were in the other app, with the playback position correctly advanced.
