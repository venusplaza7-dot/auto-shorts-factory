// This runs when you visit venus13.vercel.app
// It scrapes trending TITLES only, not videos (copyright safe)

export default async function handler(req, res) {
  const YT_KEY = process.env.YT_API_KEY;
  
  // Get trending titles
  const response = await fetch(
    `https://www.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&regionCode=US&maxResults=5&key=${YT_KEY}`
  );
  const data = await response.json();
  
  const ideas = data.items.map(v => ({
    originalTitle: v.snippet.title,
    channel: v.snippet.channelTitle,
    // Rewrite to original script - this is what makes it copyright safe
    newScript: `Breaking: ${v.snippet.title}. Here's my take: This challenge was insane, here's why it went viral and what you can learn...`,
    status: "READY_TO_GENERATE"
  }));

  return res.status(200).json({
    scraped: new Date(),
    count: ideas.length,
    ideas: ideas,
    nextStep: "【entity-GitHub¦canonical_name=GitHub】 Action will now generate video from these titles using 【entity-Pexels¦canonical_name=Pexels】 stock + AI voice"
  });
}
