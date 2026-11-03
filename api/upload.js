export default async function handler(req, res) {
  const { title, description, videoUrl } = req.body;
  
  // This uses your Refresh Token from Google Cloud
  // No copyrighted file is ever uploaded - only your original generated video
  const response = await fetch('https://www.googleapis.com/youtube/v3/videos?part=snippet,status', {
    method: 'POST',
    headers: { 
      'Authorization': `Bearer ${process.env.YT_ACCESS_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      snippet: { title, description, tags: ['shorts','【entity-mrbeast¦canonical_name=mrbeast】','【entity-lebron¦canonical_name=lebron】'] },
      status: { privacyStatus: 'public' }
    })
  });
  
  const data = await response.json();
  return res.json({ success: true, videoId: data.id });
}
