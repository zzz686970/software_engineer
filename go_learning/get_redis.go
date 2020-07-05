package main
import(
	"log"
	"github.com/go-redis/redis"
)

func main(){
	client := redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
		Password: "",
		DB: 14,
		})

	tags := map[string]float64{
		"python":   3,
		"memcache": 1,
		"rust":     2,
		"c":        1,
		"redis":    1,
		"software": 1,
		"docker":   1,
		"go":       1,
		"linux":    1,
		"flask":    1,
	}
	for tag, score := range tags {
		_, err := client.ZAdd("tags", redis.Z{score, tag}).Result()
		if err != nil {
			log.Fatalf("Error adding %s", tag)
		}
	}

	result, err := client.ZRevRangeWithScores("tags", 0, 4).Result()

	if err != nil {
		log.Fatalf("Error retrieving top 5 keys: %v", err)
	}
	if _, zItem := range result{
		log.Printf("%v\n", zItem)
	}
}