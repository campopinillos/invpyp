# invpyp

Steps to deploy on gcp cloud run:

gcloud builds submit --tag gcr.io/inversionpyp-7db7c/positiva-invpyp --project=inversionpyp-7db7c

gcloud run deploy --image gcr.io/inversionpyp-7db7c/positiva-invpyp --platform managed --project=inversionpyp-7db7c --allow-unauthenticated