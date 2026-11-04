import { google } from 'googleapis';
import fs from 'fs';

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();
  
  const oauth2Client = new google.auth.OAuth2(
    process.env.GOOGLE_CLIENT_ID,
    process.env.GOOGLE_CLIENT_SECRET,
    process.env.GOOGLE_REDIRECT_URI || 'https://developers.google.com/oauthplayground'
  );
  
  oauth2Client.setCredentials({ refresh_token: process.env.GOOGLE_REFRESH_TOKEN });
  const youtube = google.youtube({ version: 'v3', auth: oauth2Client });

  const { title, description, videoPath } = req.body;

  const response = await youtube.videos.insert({
    part: ['snippet,status'],
    requestBody: {
      snippet: {
        title: title,
        description: description,
        tags: ['shorts','reaction','commentary'],
        categoryId: '22'
      },
      status: { privacyStatus: 'private' }
    },
    media: videoPath ? { body: fs.createReadStream(videoPath) } : undefined
  });

  res.json({ success: true, videoId: response.data.id });
}
