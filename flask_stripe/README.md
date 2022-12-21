# Stripe
1. Every thing in stripe follows request response pattern.
    - stripe might need to contact if there is error or when something is happen on api.
        - eg: payment paid-> subs before it is failed to pay using web hooks.
        - web hooks allows to listen to diff (imp) events in stripe api.
            - eg : if any payment failed, stripe notified with json, what went wrong.
2. publishable key
    - safe to expose (frontend), which identifies the project.
3. https://github.com/stripe-samples/accept-a-payment/tree/main/payment-element