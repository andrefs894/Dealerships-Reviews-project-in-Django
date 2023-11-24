const express = require('express');
const app = express();
const port = process.env.PORT || 5000;
const Cloudant = require('@cloudant/cloudant');

// cloudant connection with IAM authentication
async function dbCloudantConnect() {
    try {
        const cloudant = Cloudant({
            plugins: { iamauth: { iamApiKey: 'uFeWPUC_w6Qg79y295QN_8TS6Pd8WBAoj9QvIFbSPFBC' } }, 
            url: 'https://b69568f1-7faa-40da-a28a-905167584d3d-bluemix.cloudantnosqldb.appdomain.cloud',
        });

        const db = cloudant.use('reviews');
        console.info('Connect success! Connected to DB');
        return db;
    } catch (err) {
        console.error('Connect failure: ' + err.message + ' for Cloudant DB');
        throw err;
    }
}

let db;

(async () => {
    db = await dbCloudantConnect();
})();

app.use(express.json());

// define a route to get all dealerships
app.get('/reviews/get', (req, res) => {
    const { state, dealership } = req.query;

    // create a selector object based on query parameters
    const selector = {};
    if (state) {
        selector.state = state;
    }
    
    if (dealership) {
        selector.dealership = parseInt(dealership);
    }

    const queryOptions = {
        selector,
        limit: 20,
    };

    db.find(queryOptions, (err, body) => {
        if (err) {
            console.error('Error fetching dealerships:', err);
            res.status(500).json({ error: 'An error occurred while fetching dealerships.' });
        } else {
            const dealerships = body.docs;
            res.json(dealerships);
        }
    });
});

app.post('/reviews/post', (req, res) => {
    if (!req.body) {
      return res.status(400).json({ message: 'Invalid JSON data' });
    }
  
    // extract review data from request body
    const reviewData = req.body;
  
    // save review data in db
    db.insert(reviewData, (error, newDocument) => {
        if (error) {
            return res.status(500).json({ message: 'Error saving data' });
        }
        if (newDocument.ok) {
            return res.json({ message: 'Data saved successfully' });
        } else {
            return res.json({ message: 'Failed to save data' });
        }
    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
