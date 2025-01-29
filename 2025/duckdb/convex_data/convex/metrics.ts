import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

export const retrieve = query({
  args: {},
  handler: async (ctx) => {
    return ctx.db.query("metrics").order("desc").take(50);
  },
});

export const insert = mutation({
  args: {
    name: v.string(),
    value: v.number(),
  },
  handler: async (ctx, args) => {
    await ctx.db.insert("metrics", args);
  },
});